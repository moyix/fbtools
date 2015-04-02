#!/usr/bin/env python

import IPython
import hid
import time
import fbpacket as fb
from fbpacket import Container
from operator import attrgetter

VID = 0x2687
PID = 0xfb01

beginServiceDiscovery = fb.HID_CtrlOutStartDiscovery.build(
    Container(
        hdr = Container(
            length = fb.HID_CtrlOutStartDiscovery.sizeof(),
            opcode = 'HID_CTRL_OUT_START_DISCOVERY',
        ),
        serviceUUID = 64256,
        rxPortUUID = 64258,
        baseUUID = [186, 86, 137, 166, 250, 191, 162, 189, 1, 70, 125, 110, 0, 0, 171, 173],
        txPortUUID = 64257,
        scanDuration = 5000,
    )
)

def establishLinkEx(addr):
    return fb.HID_CtrlOutEstablishLinkEx.build(
        Container(
            hdr = Container(
                length = fb.HID_CtrlOutEstablishLinkEx.sizeof(),
                opcode = 'HID_CTRL_OUT_ESTABLISH_LINK_EX',
            ),
            addr = addr,
            addrType = 1,
            minConnInterval = 6,
            maxConnInterval = 6,
            slaveLatency = 0,
            connTimeout = 200,
        )
    )

def setTX(state):
    return fb.HID_CtrlOutEnableTxPipe.build(
        Container(
            hdr = Container(
                length = fb.HID_CtrlOutEnableTxPipe.sizeof(),
                opcode = 'HID_CTRL_OUT_ENABLE_TX_PIPE',
            ),
            enable=state,
        )
    )

enableTX = setTX(True)

disableTX = setTX(False)

def setTransmitterPower(power):
    return fb.HID_CtrlOutSetTransmitterPower.build(
        Container(
            hdr = Container(
                length = fb.HID_CtrlOutSetTransmitterPower.sizeof(),
                opcode = 'HID_CTRL_OUT_SET_TRANSMITTER_POWER',
                ),
            transmitterPower = power,
        )
    )

forceDisconnect = fb.HID_CtrlOutForceDisconnect.build(
    Container(
        hdr = Container(
            length = fb.HID_CtrlOutForceDisconnect.sizeof(),
            opcode = 'HID_CTRL_OUT_FORCE_DISCONNECT',
        )
    )
)

enableFirmware = fb.HID_CtrlOutEnableFirmware.build(
    Container(
        hdr = Container(
            length = fb.HID_CtrlOutEnableFirmware.sizeof(),
            opcode = 'HID_CTRL_OUT_ENABLE_FIRMWARE',
        ),
        invertedSecurityCode = ~fb.ENABLE_IMAGE_SECURITY_CODE & 0xFFFFFFFF,
        securityCode = fb.ENABLE_IMAGE_SECURITY_CODE,
    )
)

destroyFirmware = fb.HID_CtrlOutDestroyImage.build(
    Container(
        hdr = Container(
            length = fb.HID_CtrlOutDestroyImage.sizeof(),
            opcode = 'HID_CTRL_OUT_DESTROY_IMAGE',
        ),
        securityCode = fb.DESTROY_IMAGE_SECURITY_CODE,
        invertedSecurityCode = ~fb.DESTROY_IMAGE_SECURITY_CODE & 0xFFFFFFFF,
    )
)

initAirlink = fb.make_data_packet(fb.RF_InitAirlink.build(
    Container(
        hdr = Container(
            rsvd = 0,
            group = 'RF_PKT_GRP_MISC',
            opcode = 'RF_PKT_MISC_INIT_AIRLINK'
        ),
        majorHostVersion = 10,
        minorHostVersion = 4,
        minConnInterval = 6,
        maxConnInterval = 6,
        slaveLatency = 0,
        connTimeout = 200
    )
))

readTrackerBlock = fb.make_data_packet(fb.RF_ReadTrackerBlockPkt.build(
    Container(
        hdr = Container(
            rsvd = 0,
            group = 'RF_PKT_GRP_READ',
            opcode = 'RF_PKT_READ_TRACKER_BLOCK'
        ),
        rsvd = 0,
        blockType = 'RF_TRACKERBLOCK_MEGA_DUMP'
    )
))

def readTrackerMemory(start, size):
    return fb.make_data_packet(fb.RF_ReadTrackerMemoryPkt.build(
        Container(
            hdr = Container(
                rsvd = 0,
                group = 'RF_PKT_GRP_READ',
                opcode = 'RF_PKT_READ_TRACKER_MEMORY'
            ),
            startAddr = start,
            numBytesToRead = size,
        )
    ))

def setTrackerTime(gmtTime):
    return fb.make_data_packet(fb.RF_SetDeviceClockPkt.build(
        Container(
            hdr = Container(
                rsvd = 0,
                group = 'RF_PKT_GRP_MISC',
                opcode = 'RF_PKT_MISC_SET_DEVICE_CLOCK'
            ),
            gmtTime = gmtTime,
        )
    ))

def trackerEcho(payload):
    return fb.make_data_packet(fb.RF_EchoPkt.build(
        Container(
            hdr = Container(
                rsvd = 0,
                group = 'RF_PKT_GRP_MISC',
                opcode = 'RF_PKT_MISC_ECHO_PACKET'
            ),
            payloadBytes = payload + '\0'*(16-len(payload)),
        )
    ))



def get_devs():
    fb_devs = hid.enumerate(VID, PID)
    assert len(fb_devs) == 2
    devs = []
    for d in fb_devs:
        dev = hid.device()
        dev.open_path(d['path'])
        devs.append(dev)

    # Detect control interface
    devs[0].write([2,1]) # Get Version
    resp = devs[0].read(32, timeout_ms=500)
    if resp:
        CtrlIF, DataIF = devs
    else:
        DataIF, CtrlIF = devs
    return CtrlIF, DataIF

def send_and_wait(msg, interface, handler):
    results = []
    interface.write([ord(c) for c in msg])
    while True:
        x = interface.read(32, timeout_ms=2500)
        if not x:
            time.sleep(.5)
            x = interface.read(32, timeout_ms=2500)
            if not x:
                break

        response = ''.join(chr(c) for c in x)
        res = handler(response)
        if res: results.append(res)
    return results

def recv_all(interface, handler):
    results = []
    while True:
        x = interface.read(32, timeout_ms=2500)
        if not x:
            time.sleep(.5)
            x = interface.read(32, timeout_ms=2500)
            if not x:
                break

        response = ''.join(chr(c) for c in x)
        res = handler(response)
        if res: results.append(res)
    return results

def print_tracker_info(response):
    print "  addrType:    %d" % response.addrType
    print "  address:     %s" % response.addr
    print "  RSSI:        %d" % response.rssi
    print "  serviceUUID: %d" % response.serviceUUID
    print "  serviceData: %s" % str(''.join(chr(x) for x in response.serviceData).encode('hex'))
    print "  serviceData: %s" % str(fb.RF_ServiceData.parse(''.join(chr(x) for x in response.serviceData)))

def generic_handler(response):
    response = fb.parse_hid_IN(response)
    if response.hdr.opcode == 'HID_CTRL_IN_TRACE_MSG':
        print "TRACE:", response.message[:response.message.find('\x00')]
    elif  response.hdr.opcode == 'HID_CTRL_IN_TRACKER_DEVICE_INFO':
        print "Found tracker:"
        print_tracker_info(response)
    elif response.hdr.opcode == 'HID_CTRL_IN_DISCOVERY_COMPLETE':
        print "Discovery done, found %d trackers" % response.numTrackers
    else:
        print response

def generic_data_handler(response):
    print "DATA IN:", response.encode('hex')
    try:
        parsed = fb.RF_PktHdr.parse(response)
        print parsed
    except fb.ConstructError:
        pass

def discover_handler(response):
    generic_handler(response)
    response = fb.parse_hid_IN(response)
    if response.hdr.opcode == 'HID_CTRL_IN_TRACKER_DEVICE_INFO':
        return response

def connect_to_tracker(ctrl, data):
    print "Disconnecting..."
    send_and_wait(forceDisconnect, ctrl, generic_handler)
    print "Setting TX power to maximum."
    send_and_wait(setTransmitterPower('TRANSMITTER_POWER_MAXIMUM'), ctrl, generic_handler)
    trackers = send_and_wait(beginServiceDiscovery, ctrl, discover_handler)
    if not trackers:
        print "No trackers available, won't connect."
        return False
    trackers.sort(key=attrgetter('rssi'))
    send_and_wait(establishLinkEx(trackers[0].addr), ctrl, generic_handler)
    send_and_wait(enableTX, ctrl, generic_handler)
    recv_all(data, generic_data_handler)

CtrlIF, DataIF = get_devs()

IPython.embed()
