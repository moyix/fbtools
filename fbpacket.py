#!/usr/bin/env python

from construct import *
from construct.protocols.layer2.ethernet import MacAddress
from cStringIO import StringIO

HID_REPORT_SIZE = 32
HID_MAX_SERVICE_DATA_BYTES = 6
RF_MAX_PACKET_SIZE = 20

HID_CTRL_OUT_OPCODE = Enum(ULInt8("HID_CTRL_OUT_OPCODE"),
    HID_CTRL_OUT_ECHO_REQUEST = 0,
    HID_CTRL_OUT_QUERY_VERSION = 1,
    HID_CTRL_OUT_FORCE_DISCONNECT = 2,
    HID_CTRL_OUT_SET_TRACE_LEVEL = 3,
    HID_CTRL_OUT_START_DISCOVERY = 4,
    HID_CTRL_OUT_CANCEL_DISCOVERY = 5,
    HID_CTRL_OUT_ESTABLISH_LINK = 6,
    HID_CTRL_OUT_TERMINATE_LINK = 7,
    HID_CTRL_OUT_ENABLE_TX_PIPE = 8,
    HID_CTRL_OUT_DESTROY_IMAGE = 9,
    HID_CTRL_OUT_TEST_TRANSMITTER = 10,
    HID_CTRL_OUT_TEST_RECEIVER = 11,
    HID_CTRL_OUT_TEST_END = 12,
    HID_CTRL_OUT_SET_TRANSMITTER_POWER = 13,
    HID_CTRL_OUT_START_SAMPLING_RSSI = 14,
    HID_CTRL_OUT_STOP_SAMPLING_RSSI = 15,
    HID_CTRL_OUT_READ_RSSI = 16,
    HID_CTRL_OUT_QUERY_STATE = 17,
    HID_CTRL_OUT_ESTABLISH_LINK_EX = 18,
    HID_CTRL_OUT_ESTABLISH_LINK_EX2 = 19,
    HID_CTRL_OUT_DISCOVER_CHARS = 20,
    HID_CTRL_OUT_WRITE_CHAR = 21,
    HID_CTRL_OUT_SET_RECEIVER_GAIN = 22,
    HID_CTRL_OUT_QUERY_FEATURE_BITS = 23,
    HID_CTRL_OUT_SET_FEATURE_BITS = 24,
    HID_CTRL_OUT_CLEAR_FEATURE_BITS = 25,
    HID_CTRL_OUT_READ_FLASH_DATA = 248,
    HID_CTRL_OUT_WRITE_FLASH_DATA = 249,
    HID_CTRL_OUT_ERASE_FLASH_DATA = 250,
    HID_CTRL_OUT_ENABLE_FIRMWARE = 251,
    HID_CTRL_OUT_REBOOT = 252,
    HID_CTRL_OUT_QUERY_BOOTLOADER_VERSION = 253,
)

HID_CTRL_IN_OPCODE = Enum(ULInt8("HID_CTRL_IN_OPCODE"),
    HID_CTRL_IN_ECHO_RESPONSE = 0,
    HID_CTRL_IN_TRACE_MSG = 1,
    HID_CTRL_IN_DISCOVERY_COMPLETE = 2,
    HID_CTRL_IN_TRACKER_DEVICE_INFO = 3,
    HID_CTRL_IN_LINK_ESTABLISHED = 4,
    HID_CTRL_IN_LINK_TERMINATED = 5,
    HID_CTRL_IN_LINK_PARAMETER_UPDATE = 6,
    HID_CTRL_IN_SERVICES_DETECTED = 7,
    HID_CTRL_IN_VERSION_RESPONSE = 8,
    HID_CTRL_IN_RSSI_DATA = 9,
    HID_CTRL_IN_ALREADY_CONNECTED = 10,
    HID_CTRL_IN_DISCOVERED_SVC_128 = 11,
    HID_CTRL_IN_DISCOVERED_SVC_16 = 12,
    HID_CTRL_IN_DISCOVERED_CHR_128 = 13,
    HID_CTRL_IN_DISCOVERED_CHR_16 = 14,
    HID_CTRL_IN_CHR_DISCOVERY_COMPLETE = 15,
    HID_CTRL_IN_NOTIFY_CHAR = 16,
    HID_CTRL_IN_FEATURE_BITS = 17,
    HID_CTRL_IN_DATA_OUT_STATUS = 18,
    HID_CTRL_IN_READ_FLASH_DATA = 252,
    HID_CTRL_IN_BOOTLOADER_VERSION_RESPONSE = 253,
    HID_CTRL_IN_ACK_RESPONSE = 254,
    HID_CTRL_IN_NAK_RESPONSE = 255,
)

DONGLE_FEATURE_DATA_OUT_STATUS = 1
DONGLE_FEATURE_RESERVED_1 = 2
DONGLE_FEATURE_RESERVED_2 = 4
DONGLE_FEATURE_RESERVED_3 = 8
DONGLE_FEATURE_RESERVED_4 = 16
DONGLE_FEATURE_RESERVED_5 = 32
DONGLE_FEATURE_RESERVED_6 = 64
DONGLE_FEATURE_RESERVED_7 = 128
DONGLE_FEATURE_RESERVED_8 = 256
DONGLE_FEATURE_RESERVED_9 = 512
DONGLE_FEATURE_RESERVED_10 = 1024
DONGLE_FEATURE_RESERVED_11 = 2048
DONGLE_FEATURE_RESERVED_12 = 4096
DONGLE_FEATURE_RESERVED_13 = 8192
DONGLE_FEATURE_RESERVED_14 = 16384
DONGLE_FEATURE_RESERVED_15 = 32768
DONGLE_FEATURE_ALL = 65535

HID_CtrlRptHdrOut = Struct("HID_CtrlRptHdrOut",
    ULInt8("length"),
    Rename("opcode", HID_CTRL_OUT_OPCODE)
)

HID_CtrlOutEchoRequest = Struct("HID_CtrlOutEchoRequest",
    Rename("hdr", HID_CtrlRptHdrOut),
    Array(HID_REPORT_SIZE - HID_CtrlRptHdrOut.sizeof(), ULInt8("payload"))
)

HID_CtrlOutQueryVersion = Struct("HID_CtrlOutQueryVersion",
    Rename("hdr", HID_CtrlRptHdrOut)
)

HID_CtrlOutForceDisconnect = Struct("HID_CtrlOutForceDisconnect",
    Rename("hdr", HID_CtrlRptHdrOut)
)

DONGLE_TRACE_LEVEL = Enum(ULInt8("DONGLE_TRACE_LEVEL"),
    DONGLE_TRACE_LEVEL_OFF = 0,
    DONGLE_TRACE_LEVEL_ERROR = 1,
    DONGLE_TRACE_LEVEL_NORMAL = 2,
    DONGLE_TRACE_LEVEL_VERBOSE = 3
)

HID_CtrlOutSetTraceLevel = Struct("HID_CtrlOutSetTraceLevel",
    Rename("hdr", HID_CtrlRptHdrOut),
    Rename("dongleTraceLevel", DONGLE_TRACE_LEVEL)
)

HID_CtrlOutStartDiscovery = Struct("HID_CtrlOutStartDiscovery",
    Rename("hdr", HID_CtrlRptHdrOut),
    Array(16, ULInt8("baseUUID")),
    ULInt16("serviceUUID"),
    ULInt16("txPortUUID"),
    ULInt16("rxPortUUID"),
    ULInt16("scanDuration")
)

HID_CtrlOutCancelDiscovery = Struct("HID_CtrlOutCancelDiscovery",
    Rename("hdr", HID_CtrlRptHdrOut)
)

HID_CtrlOutEstablishLink = Struct("HID_CtrlOutEstablishLink",
    Rename("hdr", HID_CtrlRptHdrOut),
    MacAddress("addr"),
    ULInt8("addrType"),
    ULInt16("serviceUUID")
)

HID_CtrlOutEstablishLinkEx = Struct("HID_CtrlOutEstablishLinkEx",
    Rename("hdr", HID_CtrlRptHdrOut),
    MacAddress("addr"),
    ULInt8("addrType"),
    ULInt16("minConnInterval"),
    ULInt16("maxConnInterval"),
    ULInt16("slaveLatency"),
    ULInt16("connTimeout")
)

HID_CtrlOutTerminateLink = Struct("HID_CtrlOutTerminateLink",
    Rename("hdr", HID_CtrlRptHdrOut)
)

HID_CtrlOutEnableTxPipe = Struct("HID_CtrlOutEnableTxPipe",
    Rename("hdr", HID_CtrlRptHdrOut),
    Flag("enable")
)

HID_CtrlOutEnableFlood = Struct("HID_CtrlOutEnableFlood",
    Rename("hdr", HID_CtrlRptHdrOut),
    Flag("enableFlood")
)

DESTROY_IMAGE_SECURITY_CODE = 4050327354

HID_CtrlOutDestroyImage = Struct("HID_CtrlOutDestroyImage",
    Rename("hdr", HID_CtrlRptHdrOut),
    ULInt32("securityCode"),
    ULInt32("invertedSecurityCode")
)

DTM_TRANSMIT_PAYLOAD = Enum(ULInt8("DTM_TRANSMIT_PAYLOAD"),
    DTM_TRANSMIT_PAYLOAD_UNDEFINED = 255,
    DTM_TRANSMIT_PAYLOAD_PRBS9 = 0,
    DTM_TRANSMIT_PAYLOAD_0x0F = 1,
    DTM_TRANSMIT_PAYLOAD_0x55 = 2,
    DTM_TRANSMIT_PAYLOAD_PRBS15 = 3,
    DTM_TRANSMIT_PAYLOAD_0xFF = 4,
    DTM_TRANSMIT_PAYLOAD_0x00 = 5,
    DTM_TRANSMIT_PAYLOAD_0xF0 = 6,
    DTM_TRANSMIT_PAYLOAD_0xAA = 7,
    DTM_TRANSMIT_PAYLOAD_MAXIMUM = 8
)

TEST_TRANSMIT_TYPE = Enum(ULInt8("TEST_TRANSMIT_TYPE"),
    TEST_TRANSMIT_TYPE_HCI_LE_TRANSMITTER_TEST = 0,
    TEST_TRANSMIT_TYPE_HCI_EXT_MODEM_HOP_TEST = 1,
    TEST_TRANSMIT_TYPE_HCI_EXT_MODEM_TEST_TX_CMD_MODULATED = 2,
    TEST_TRANSMIT_TYPE_HCI_EXT_MODEM_TEST_TX_CMD_UNMODULATED = 3,
    TEST_TRANSMIT_TYPE_MAXIMUM = 4
)

TRANSMITTER_POWER = Enum(ULInt8("TRANSMITTER_POWER"),
    TRANSMITTER_POWER_MINUS_23_DBM = 0,
    TRANSMITTER_POWER_MINUS_6_DBM = 1,
    TRANSMITTER_POWER_0_DBM = 2,
    TRANSMITTER_POWER_4_DBM = 3,
    TRANSMITTER_POWER_2_DBM = 4,
    TRANSMITTER_POWER_MAXIMUM = 5
)

RECEIVER_GAIN = Enum(ULInt8("RECEIVER_GAIN"),
    RECEIVER_GAIN_STANDARD = 0,
    RECEIVER_GAIN_HIGH = 1,
    RECEIVER_GAIN_MAXIMUM = 2
)

HID_CtrlOutTestTransmitter = Struct("HID_CtrlOutTestTransmitter",
    Rename("hdr", HID_CtrlRptHdrOut),
    Rename("testTransmitType", TEST_TRANSMIT_TYPE),
    ULInt8("txFrequency"),
    ULInt8("dataLength"),
    Rename("payload", DTM_TRANSMIT_PAYLOAD)
)

TEST_RECEIVE_TYPE = Enum(ULInt8("TEST_RECEIVE_TYPE"),
    TEST_RECEIVE_TYPE_HCI_LE_RECEIVER_TEST = 0,
    TEST_RECEIVE_TYPE_HCI_EXT_MODEM_TEST = 1,
    TEST_RECEIVE_TYPE_MAXIMUM = 2
)

HID_CtrlOutTestReceiver = Struct("HID_CtrlOutTestReceiver",
    Rename("hdr", HID_CtrlRptHdrOut),
    Rename("testReceiveType", TEST_RECEIVE_TYPE),
    ULInt8("rxFrequency")
)

TEST_END_TYPE = Enum(ULInt8("TEST_END_TYPE"),
    TEST_END_TYPE_HCI_DTM_TEST = 0,
    TEST_END_TYPE_HCI_EXT_MODEM_TEST = 1,
    TEST_END_TYPE_MAXIMUM = 2
)

HID_CtrlOutTestEnd = Struct("HID_CtrlOutTestEnd",
    Rename("hdr", HID_CtrlRptHdrOut),
    Rename("testEndType", TEST_END_TYPE)
)

HID_CtrlOutSetTransmitterPower = Struct("HID_CtrlOutSetTransmitterPower",
    Rename("hdr", HID_CtrlRptHdrOut),
    Rename("transmitterPower", TRANSMITTER_POWER)
)

HID_CtrlOutStartReadingRSSI = Struct("HID_CtrlOutStartReadingRSSI",
    Rename("hdr", HID_CtrlRptHdrOut),
    ULInt16("rxSampleRateRSSI")
)

HID_CtrlOutDiscoverCharacteristics = Struct("HID_CtrlOutDiscoverCharacteristics",
    Rename("hdr", HID_CtrlRptHdrOut),
    ULInt16("startHandle"),
    ULInt16("endHandle")
)

HID_CtrlOutWriteChar = Struct("HID_CtrlOutWriteChar",
    Rename("hdr", HID_CtrlRptHdrOut),
    ULInt16("chrHandle"),
    ULInt8("length"),
    Array(RF_MAX_PACKET_SIZE, ULInt8("value"))
)

HID_CtrlOutSetReceiverGain = Struct("HID_CtrlOutSetReceiverGain",
    Rename("hdr", HID_CtrlRptHdrOut),
    Rename("receiverGain", RECEIVER_GAIN)
)

HID_CtrlOutSetFeatureBits = Struct("HID_CtrlOutSetFeatureBits",
    Rename("hdr", HID_CtrlRptHdrOut),
    ULInt16("featureBits")
)

FLASH_32_BIT_WORDS_PER_HID_RECORD = 6

HID_CtrlOutReadFlashMemory = Struct("HID_CtrlOutReadFlashMemory",
    Rename("hdr", HID_CtrlRptHdrOut),
    ULInt16("numberOf32BitWords"),
    ULInt32("flashAddress")
)

HID_CtrlOutWriteFlashMemory = Struct("HID_CtrlOutWriteFlashMemory",
    Rename("hdr", HID_CtrlRptHdrOut),
    ULInt16("numberOf32BitWords"),
    ULInt32("flashAddress"),
    Array(4 * FLASH_32_BIT_WORDS_PER_HID_RECORD, ULInt8("flashData"))
)

ENABLE_IMAGE_SECURITY_CODE = 3393963805

HID_CtrlOutEnableFirmware = Struct("HID_CtrlOutEnableFirmware",
    Rename("hdr", HID_CtrlRptHdrOut),
    ULInt32("invertedSecurityCode"),
    ULInt32("securityCode")
)

def DefaultOut(datalen):
    return Struct("HID_CTRL_OUT_DEFAULT",
        Rename("hdr", HID_CtrlRptHdrOut),
        HexDumpAdapter(String("payload", datalen - HID_CtrlRptHdrOut.sizeof()))
    )

HID_OUT_MAP = {
    "HID_CTRL_OUT_ECHO_REQUEST": HID_CtrlOutEchoRequest,
    "HID_CTRL_OUT_QUERY_VERSION": HID_CtrlOutQueryVersion,
    "HID_CTRL_OUT_FORCE_DISCONNECT": HID_CtrlOutForceDisconnect,
    "HID_CTRL_OUT_SET_TRACE_LEVEL": HID_CtrlOutSetTraceLevel,
    "HID_CTRL_OUT_START_DISCOVERY": HID_CtrlOutStartDiscovery,
    "HID_CTRL_OUT_CANCEL_DISCOVERY": HID_CtrlOutCancelDiscovery,
    "HID_CTRL_OUT_ESTABLISH_LINK": HID_CtrlOutEstablishLink,
    "HID_CTRL_OUT_TERMINATE_LINK": HID_CtrlOutTerminateLink,
    "HID_CTRL_OUT_ENABLE_TX_PIPE": HID_CtrlOutEnableTxPipe,
    "HID_CTRL_OUT_DESTROY_IMAGE": HID_CtrlOutDestroyImage,
    "HID_CTRL_OUT_TEST_TRANSMITTER": HID_CtrlOutTestTransmitter,
    "HID_CTRL_OUT_TEST_RECEIVER": HID_CtrlOutTestReceiver,
    "HID_CTRL_OUT_TEST_END": HID_CtrlOutTestEnd,
    "HID_CTRL_OUT_SET_TRANSMITTER_POWER": HID_CtrlOutSetTransmitterPower,
    "HID_CTRL_OUT_START_SAMPLING_RSSI": HID_CtrlOutStartReadingRSSI,
    "HID_CTRL_OUT_ESTABLISH_LINK_EX": HID_CtrlOutEstablishLinkEx,
    "HID_CTRL_OUT_ESTABLISH_LINK_EX2": HID_CtrlOutEstablishLinkEx,  # These use the same packet type but differ in opcode
    "HID_CTRL_OUT_DISCOVER_CHARS": HID_CtrlOutDiscoverCharacteristics,
    "HID_CTRL_OUT_WRITE_CHAR": HID_CtrlOutWriteChar,
    "HID_CTRL_OUT_SET_RECEIVER_GAIN": HID_CtrlOutSetReceiverGain,
    "HID_CTRL_OUT_SET_FEATURE_BITS": HID_CtrlOutSetFeatureBits,
    "HID_CTRL_OUT_READ_FLASH_DATA": HID_CtrlOutReadFlashMemory,
    "HID_CTRL_OUT_WRITE_FLASH_DATA": HID_CtrlOutWriteFlashMemory,
    "HID_CTRL_OUT_ENABLE_FIRMWARE": HID_CtrlOutEnableFirmware ,
}

def parse_hid_OUT(data):
    """Parses a message sent TO the dongle"""
    # Trim
    #data = data[:ord(data[0])]
    
    opCode = ord(data[1])
    opStr = HID_CTRL_OUT_OPCODE.decoding[opCode]

    PktType = HID_OUT_MAP.get(opStr, None)
    
    if PktType is None:
        PktType = DefaultOut(len(data))

    return PktType.parse_stream(StringIO(data))


HID_CtrlRptHdrIn = Struct("HID_CtrlRptHdrIn",
    ULInt8("length"),
    Rename("opcode", HID_CTRL_IN_OPCODE)
)

HID_CtrlInEchoResponse = Struct("HID_CtrlInEchoResponse",
    Rename("hdr", HID_CtrlRptHdrIn),
    Array(HID_REPORT_SIZE - HID_CtrlRptHdrIn.sizeof(), ULInt8("payload"))
)

HID_CtrlInTraceMsg = Struct("HID_CtrlInTraceMsg",
    Rename("hdr", HID_CtrlRptHdrIn),
    String("message", HID_REPORT_SIZE - HID_CtrlRptHdrIn.sizeof())
)

HID_CtrlInDiscoveryComplete = Struct("HID_CtrlInDiscoveryComplete",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt8("numTrackers")
)

HID_CtrlInTrackerDeviceInfo = Struct("HID_CtrlInTrackerDeviceInfo",
    Rename("hdr", HID_CtrlRptHdrIn),
    MacAddress("addr"),
    ULInt8("addrType"),
    SLInt8("rssi"),
    ULInt8("serviceDataLen"),
    Array(HID_MAX_SERVICE_DATA_BYTES, ULInt8("serviceData")),
    ULInt16("serviceUUID")
)

HID_CtrlInLinkEstablished = Struct("HID_CtrlInLinkEstablished",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt8("linkStatus")
)

HID_CtrlInLinkTerminated = Struct("HID_CtrlInLinkTerminated",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt8("reason")
)

HID_CtrlInLinkParameterUpdate = Struct("HID_CtrlInLinkParameterUpdate",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt16("connInterval"),
    ULInt16("connLatency"),
    ULInt16("connTimeout")
)

HID_CtrlInServicesDetected = Struct("HID_CtrlInServicesDetected",
    Rename("hdr", HID_CtrlRptHdrIn)
)

MICROCONTROLLER = Enum(ULInt8("MICROCONTROLLER"),
    MICROCONTROLLER_UNKNOWN = 0,
    MICROCONTROLLER_CC2540F256 = 1,
    MICROCONTROLLER_CC2540F128 = 2,
    MICROCONTROLLER_TOTAL = 3
)

HID_CtrlInVersionResponse = Struct("HID_CtrlInVersionResponse",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt8("majorVersion"),
    ULInt8("minorVersion"),
    MacAddress("deviceAddr"),
    ULInt16("flashEraseTime"),
    ULInt32("firmwareStartAddress"),
    ULInt32("firmwareEndAddress"),
    Rename("ccIC", MICROCONTROLLER)
)

VERSION_RESPONSE_LEGACY_PKT_SIZE = 21

HID_CtrlInVersionResponseEx = Struct("HID_CtrlInVersionResponseEx",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt8("majorVersion"),
    ULInt8("minorVersion"),
    MacAddress("deviceAddr"),
    ULInt16("flashEraseTime"),
    ULInt32("firmwareStartAddress"),
    ULInt32("firmwareEndAddress"),
    Rename("ccIC", MICROCONTROLLER),
    ULInt8("hardwareRevision")
)

HID_CtrlInReadFlashMemory = Struct("HID_CtrlInReadFlashMemory",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt16("numberOf32BitWords"),
    ULInt32("flashAddress"),
    Array(4 * FLASH_32_BIT_WORDS_PER_HID_RECORD, ULInt8("flashData"))
)

HID_CtrlInBootloaderVersionResponse = Struct("HID_CtrlInBootloaderVersionResponse",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt8("majorVersion"),
    ULInt8("minorVersion"),
    MacAddress("deviceAddr"),
    ULInt16("flashEraseTime"),
    ULInt32("firmwareStartAddress"),
    ULInt32("firmwareEndAddress"),
    Rename("ccIC", MICROCONTROLLER)
)

HID_CtrlInRSSI = Struct("HID_CtrlInRSSI",
    Rename("hdr", HID_CtrlRptHdrIn),
    SLInt8("rssi")
)

ERROR_CODES = {
    0: "Success",
    2: "Unknown Connection Identifier",
    6: "Pin or Key Missing",
    7: "Memory Capacity Exceeded",
    8: "Connection Timeout",
    9: "Connection Limit Exceeded",
    12: "Command Disallowed",
    13: "Command Rejected Due To Limited Resources",
    17: "Unsupported Feature or Parameter Value",
    18: "Invalid HCI Command Parameters",
    18: "Invalid HCI Command Parameters or 0x30: Parameter Out of Mandatory Range?",
    19: "Remote User Terminated Connection",
    20: "Remote Device Terminated Connection Due To Low Resources",
    21: "Remote Device Terminated Connection Due To Power Off",
    22: "Connection Terminated By Local Host",
    26: "Unsupported Remote Feature",
    31: "Unspecified Error",
    33: "Role Change Not Allowed",
    34: "Link Layer Response Timeout",
    40: "Instant Passed",
    48: "Parameter Out Of Mandatory Range",
    58: "Controller Busy",
    59: "Unacceptable Connection Interval",
    60: "Directed Advertising Timeout",
    61: "Connection Terminated Due To MIC Failure",
    62: "Connection Failed To Be Established",
    63: "MAC Connection Failed",
}

HID_CtrlInNakResponse = Struct("HID_CtrlInNakResponse",
    Rename("hdr", HID_CtrlRptHdrIn),
    Optional(ULInt16("errorCode"))
)

HID_CtrlInDiscoveredSvc128 = Struct("HID_CtrlInDiscoveredSvc128",
    Rename("hdr", HID_CtrlRptHdrIn),
    Array(16, ULInt8("serviceUUID")),
    ULInt16("startHandle"),
    ULInt16("endHandle")
)

HID_CtrlInDiscoveredSvc16 = Struct("HID_CtrlInDiscoveredSvc16",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt16("serviceUUID"),
    ULInt16("startHandle"),
    ULInt16("endHandle")
)

HID_CtrlInDiscoveredChr128 = Struct("HID_CtrlInDiscoveredChr128",
    Rename("hdr", HID_CtrlRptHdrIn),
    Array(16, ULInt8("chrUUID")),
    ULInt16("chrHandle")
)

HID_CtrlInDiscoveredChr16 = Struct("HID_CtrlInDiscoveredChr16",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt16("chrUUID"),
    ULInt16("chrHandle")
)

HID_CtrlInNotifyChar = Struct("HID_CtrlInNotifyChar",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt16("chrHandle"),
    ULInt8("length"),
    Array(RF_MAX_PACKET_SIZE, ULInt8("value"))
)

HID_CtrlInFeatureBits = Struct("HID_CtrlInFeatureBits",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt16("featureBits")
)

HID_CtrlInDataOutStatus = Struct("HID_CtrlInDataOutStatus",
    Rename("hdr", HID_CtrlRptHdrIn),
    ULInt8("status")
)

def DefaultIn(datalen):
    return Struct("HID_CTRL_IN_DEFAULT",
        Rename("hdr", HID_CtrlRptHdrIn),
        HexDumpAdapter(String("payload", datalen - HID_CtrlRptHdrIn.sizeof()))
    )

HID_IN_MAP = {
    'HID_CTRL_IN_ECHO_RESPONSE': HID_CtrlInEchoResponse,
    'HID_CTRL_IN_TRACE_MSG': HID_CtrlInTraceMsg,
    'HID_CTRL_IN_DISCOVERY_COMPLETE': HID_CtrlInDiscoveryComplete,
    'HID_CTRL_IN_TRACKER_DEVICE_INFO': HID_CtrlInTrackerDeviceInfo,
    'HID_CTRL_IN_LINK_ESTABLISHED': HID_CtrlInLinkEstablished,
    'HID_CTRL_IN_LINK_TERMINATED': HID_CtrlInLinkTerminated,
    'HID_CTRL_IN_LINK_PARAMETER_UPDATE': HID_CtrlInLinkParameterUpdate,
    'HID_CTRL_IN_SERVICES_DETECTED': HID_CtrlInServicesDetected,
    'HID_CTRL_IN_RSSI_DATA': HID_CtrlInRSSI,
    'HID_CTRL_IN_DISCOVERED_SVC_128': HID_CtrlInDiscoveredSvc128,
    'HID_CTRL_IN_DISCOVERED_SVC_16': HID_CtrlInDiscoveredSvc16,
    'HID_CTRL_IN_DISCOVERED_CHR_128': HID_CtrlInDiscoveredChr128,
    'HID_CTRL_IN_DISCOVERED_CHR_16': HID_CtrlInDiscoveredChr16,
    'HID_CTRL_IN_NOTIFY_CHAR': HID_CtrlInNotifyChar,
    'HID_CTRL_IN_FEATURE_BITS': HID_CtrlInFeatureBits,
    'HID_CTRL_IN_DATA_OUT_STATUS': HID_CtrlInDataOutStatus,
    'HID_CTRL_IN_READ_FLASH_DATA': HID_CtrlInReadFlashMemory,
    'HID_CTRL_IN_BOOTLOADER_VERSION_RESPONSE': HID_CtrlInBootloaderVersionResponse,
    'HID_CTRL_IN_NAK_RESPONSE': HID_CtrlInNakResponse,
}

def parse_hid_IN(data):
    """Parses a message received FROM the dongle"""
    # Trim
    data = data[:ord(data[0])]
    
    opCode = ord(data[1])
    opStr = HID_CTRL_IN_OPCODE.decoding[opCode]

    # Special case
    if opStr == 'HID_CTRL_IN_VERSION_RESPONSE':
        if len(data) <= VERSION_RESPONSE_LEGACY_PKT_SIZE:
            PktType = HID_CtrlInVersionResponse
        else:
            PktType = HID_CtrlInVersionResponseEx
    else:
        PktType = HID_IN_MAP.get(opStr, None)
    
    if PktType is None:
        PktType = DefaultIn(len(data))

    return PktType.parse_stream(StringIO(data))

# RF layer
# ========

RF_PKT_MAGIC_BYTE = '\xC0'

RF_PKT_ESCAPE_BYTE = 219
RF_PKT_ESCAPE1_BYTE = 220
RF_PKT_ESCAPE2_BYTE = 221

RF_PKT_GRP = Enum(BitField("RF_PKT_GRP", 3),
    RF_PKT_GRP_MISC = 0,
    RF_PKT_GRP_READ = 1,
    RF_PKT_GRP_UPDATE = 2,
    RF_PKT_GRP_RESERVED_1 = 3,
    RF_PKT_GRP_XFR2HOST = 4,
    RF_PKT_GRP_XFR2TRACKER = 5,
    RF_PKT_GRP_RESERVED_2 = 6,
    RF_PKT_GRP_RESERVED_3 = 7,
)

RF_PKT_MISC = Enum(BitField("RF_PKT_MISC", 4),
    RF_PKT_MISC_POLL_HOST = 0,
    RF_PKT_MISC_RESET_LINK = 1,
    RF_PKT_MISC_CMD_ACK = 2,
    RF_PKT_MISC_CMD_NAK = 3,
    RF_PKT_MISC_SET_DEVICE_CLOCK = 4,
    RF_PKT_MISC_RESERVED_5 = 5,
    RF_PKT_MISC_ALERT_USER = 6,
    RF_PKT_MISC_RESERVED_7 = 7,
    RF_PKT_MISC_USER_ACTIVITY = 8,
    RF_PKT_MISC_ECHO_PACKET = 9,
    RF_PKT_MISC_INIT_AIRLINK = 10,
    RF_PKT_MISC_BTH_RX_ACK = 11,
)

RF_PKT_READ = Enum(BitField("RF_PKT_READ", 4),
    RF_PKT_READ_TRACKER_BLOCK = 0,
    RF_PKT_READ_TRACKER_MEMORY = 1,
    RF_PKT_READ_FIRST_HOST_BLOCK = 2,
    RF_PKT_READ_NEXT_HOST_BLOCK = 3,
    RF_PKT_READ_AIRLINK_BLOCK = 4,
)

RF_PKT_UPDATE = Enum(BitField("RF_PKT_UPDATE", 4),
    RF_PKT_UPDATE_RESERVED_1 = 0,
    RF_PKT_UPDATE_RESERVED_2 = 1,
    RF_PKT_UPDATE_BEACON_PARAMS = 2,
    RF_PKT_UPDATE_SECRET = 3,
    RF_PKT_UPDATE_TRACKER_BLOCK = 4,
)

RF_PKT_XFR2HOST = Enum(BitField("RF_PKT_XFR2HOST", 4),
    RF_PKT_XFR2HOST_SINGLE_BLOCK = 0,
    RF_PKT_XFR2HOST_STREAM_STARTING = 1,
    RF_PKT_XFR2HOST_STREAM_FINISHED = 2,
)

RF_PKT_XFR2TRACKER = Enum(BitField("RF_PKT_XFR2TRACKER", 4),
    RF_PKT_XFR2TRACKER_SINGLE_BLOCK = 0,
    RF_PKT_XFR2TRACKER_STREAM_STARTING = 1,
    RF_PKT_XFR2TRACKER_STREAM_FINISHED = 2,
)

SITE_PROTOCOL_MEGA_DUMP = 500
SITE_PROTOCOL_RESERVED1 = 501
SITE_PROTOCOL_BSL_BLOB = 502
SITE_PROTOCOL_APP_BLOB = 503
SITE_PROTOCOL_MICRO_DUMP = 510

SITE_CMD_RESERVED = 0
SITE_CMD_DELETE_MINUTE_SUMMARIES = 1
SITE_CMD_DELETE_ANNOTATIONS = 2
SITE_CMD_DELETE_USAGE_RECORDS = 3
SITE_CMD_DELETE_DAILY_SUMMARIES = 4
SITE_CMD_SET_TRACKER_CLOCK = 5
SITE_CMD_SET_SYNC_DELAY_MINUTES = 6
SITE_CMD_DELETE_ALTITUDE_RECORDS = 7

RF_BootMode = Enum(ULInt8("RF_BootMode"),
    RF_BOOTMODE_APP = 0,
    RF_BOOTMODE_BSL = 1
)

RF_TrackerBlock = Enum(BitField("RF_TrackerBlock", 4),
    RF_TRACKERBLOCK_RESERVED_1 = 0,
    RF_TRACKERBLOCK_MICRO_DUMP_RESP_2 = 1,
    RF_TRACKERBLOCK_BOND_DATA = 2,
    RF_TRACKERBLOCK_MICRO_DUMP = 3,
    RF_TRACKERBLOCK_MEGA_DUMP_RESPONSE = 4,
    RF_TRACKERBLOCK_RESERVED_4 = 5,
    RF_TRACKERBLOCK_RESERVED_5 = 6,
    RF_TRACKERBLOCK_RESERVED_6 = 7,
    RF_TRACKERBLOCK_MICRO_DUMP_RESPONSE = 8,
    RF_TRACKERBLOCK_MEMORY = 9,
    RF_TRACKERBLOCK_RESERVED_A = 10,
    RF_TRACKERBLOCK_RESERVED_B = 11,
    RF_TRACKERBLOCK_AIRLINK_INFO = 12,
    RF_TRACKERBLOCK_MEGA_DUMP = 13
)

RF_PktHdr = Struct("RF_PktHdr",
    Magic(RF_PKT_MAGIC_BYTE),
    EmbeddedBitStruct(
        BitField("rsvd", 1),
        Rename("group", RF_PKT_GRP),
        Switch("opcode", lambda ctx: ctx.group,
            {
                'RF_PKT_GRP_MISC': RF_PKT_MISC,
                'RF_PKT_GRP_READ': RF_PKT_READ,
                'RF_PKT_GRP_UPDATE': RF_PKT_UPDATE,
                'RF_PKT_GRP_XFR2HOST': RF_PKT_XFR2HOST,
                'RF_PKT_GRP_XFR2TRACKER': RF_PKT_XFR2TRACKER,
            },
            default = BitField("opcode", 4),
        ),
    )
)

RF_CmdNakPkt = Struct("RF_CmdNakPkt",
    Rename("hdr", RF_PktHdr),
    ULInt16("errorCode")
)

RF_SetDeviceClockPkt = Struct("RF_SetDeviceClockPkt",
    Rename("hdr", RF_PktHdr),
    ULInt32("gmtTime")
)

RF_EchoPkt = Struct("RF_EchoPkt",
    Rename("hdr", RF_PktHdr),
    Bytes("payloadBytes", 16)
)

RF_InitAirlink = Struct("RF_InitAirlink",
    Rename("hdr", RF_PktHdr),
    ULInt8("majorHostVersion"),
    ULInt8("minorHostVersion"),
    ULInt16("minConnInterval"),
    ULInt16("maxConnInterval"),
    ULInt16("slaveLatency"),
    ULInt16("connTimeout")
)

RF_ReadTrackerBlockPkt = Struct("RF_ReadTrackerBlockPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    )
)

RF_ReadTrackerMemoryPkt = Struct("RF_ReadTrackerMemoryPkt",
    Rename("hdr", RF_PktHdr),
    ULInt32("startAddr"),
    ULInt32("numBytesToRead")
)

RF_ReadFirstHostBlockPkt_Legacy = Struct("RF_ReadFirstHostBlockPkt_Legacy",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("seqNum", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt16("numBytesToRead")
)

RF_ReadFirstHostBlockPkt = Struct("RF_ReadFirstHostBlockPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("seqNum", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt16("numBytesToRead"),
    ULInt8("windowSize")
)

RF_ReadNextHostBlockPkt = Struct("RF_ReadNextHostBlockPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("seqNum", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt16("numBytesToRead"))

RF_ReadAirlinkBlockPkt = Struct("RF_ReadAirlinkBlockPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt8("majorAirlinkVersion"),
    ULInt8("minorAirlinkVersion"),
    Rename("bootMode", RF_BootMode),
    MacAddress("deviceAddress")
)

RF_ReadFastAirlinkBlockPkt = Struct("RF_ReadFastAirlinkBlockPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt8("majorAirlinkVersion"),
    ULInt8("minorAirlinkVersion"),
    Rename("bootMode", RF_BootMode),
    MacAddress("deviceAddress"),
    ULInt16("mtuSize")
)

RF_UpdateBeaconParamsPkt = Struct("RF_UpdateBeaconParamsPkt",
    Rename("hdr", RF_PktHdr),
    ULInt8("activeDuration"),
    ULInt8("activeWait"),
    ULInt8("inactiveDuration"),
    ULInt8("inactiveWait"),
    ULInt8("sessionTimeout")
)

RF_UpdateSecretPkt = Struct("RF_UpdateSecretPkt",
    Rename("hdr", RF_PktHdr),
    ULInt32("secret")
)

RF_UpdateTrackerBlockPkt_Legacy = Struct("RF_UpdateTrackerBlockPkt_Legacy",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(BitField("rsvd", 4),
    Rename("blockType", RF_TrackerBlock)),
    ULInt32("numDataBytes"),
    ULInt16("crc"))

RF_UpdateTrackerBlockPkt = Struct("RF_UpdateTrackerBlockPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt32("numDataBytes"),
    ULInt16("crc"),
    ULInt8("windowSize")
)

RF_DeleteTrackerBlockPkt = Struct("RF_DeleteTrackerBlockPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt32("gmtTime")
)

RF_Xfr2HostSingleBlockPkt = Struct("RF_Xfr2HostSingleBlockPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    Array(RF_MAX_PACKET_SIZE - 2 - 1, ULInt8("payload"))
)

RF_Xfr2HostStreamStartingPkt = Struct("RF_Xfr2HostStreamStartingPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt32("numPayloadBytes")
)

RF_Xfr2HostStreamFinishedPkt = Struct("RF_Xfr2HostStreamFinishedPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt16("crc"),
    ULInt32("numPayloadBytes")
)

RF_Xfr2TrackerSingleBlockPkt = Struct("RF_Xfr2TrackerSingleBlockPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    Array(RF_MAX_PACKET_SIZE - 2 - 1, ULInt8("payload"))
)

RF_Xfr2TrackerAirlinkInfoPkt = Struct("RF_Xfr2TrackerAirlinkInfoPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt8("majorHostVersion"),
    ULInt8("minorHostVersion"),
    Array(5, ULInt8("dataPipeAddr"))
)

RF_Xfr2TrackerStreamStartingPkt = Struct("RF_Xfr2TrackerStreamStartingPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    )
)

RF_Xfr2TrackerStreamFinishedPkt = Struct("RF_Xfr2TrackerStreamFinishedPkt",
    Rename("hdr", RF_PktHdr),
    EmbeddedBitStruct(
        BitField("rsvd", 4),
        Rename("blockType", RF_TrackerBlock)
    ),
    ULInt16("crc"),
    ULInt32("numPayloadBytes")
)

RF_AlertUserPkt = Struct("RF_AlertUserPkt",
    Rename("hdr", RF_PktHdr)
)

RF_CmdAckPkt = Struct("RF_CmdAckPkt",
    Rename("hdr", RF_PktHdr)
)

RF_ServiceData = Struct("RF_ServiceData",
    ULInt8("productId"),
    EmbeddedBitStruct(
        BitField("reserved", 1),
        BitField("colorCode", 4),
        BitField("canDisplayNumber", 1),
        BitField("synchedRecently", 1),
        BitField("specialMode", 1),
    )
)

RF_ProtocolHeader = Struct("RF_ProtocolHeader",
    ULInt32("siteProtocol"),
    ULInt16("encryptionInfo"),
    ULInt32("nonce")
)

RF_SignatureTrailer = Struct("RF_SignatureTrailer",
    ULInt32("signature64Lo"),
    ULInt32("signature64Hi"),
    ULInt16("length24Lo"),
    ULInt8("length24Hi")
)

RF_SiteCommand = Struct("RF_SiteCommand",
    ULInt8("siteCommand"),
    ULInt32("gmtTime")
)

RF_MEM_SECTION_NO_OP = 0
RF_MEM_SECTION_BSL_IMAGE = 1
RF_MEM_SECTION_APP_IMAGE = 2
RF_MEM_SECTION_REBOOT_TO_BSL = 3
RF_MEM_SECTION_REBOOT_TO_APP = 4

RF_MemorySectionHeader = Struct("RF_MemorySectionHeader",
    ULInt8("productId"),
    ULInt8("dataType"),
    ULInt32("baseAddress"),
    ULInt32("originalLength"),
    ULInt32("encodedLength"),
    ULInt16("crc16"),
    ULInt32("reserved")
)

RF_BondedStatus = Struct("RF_BondedStatus",
    ULInt8("isTrackerBonded"),
    ULInt8("isBondedToCurrentPeer"),
    ULInt8("isANCSReady"),
    Rename("serviceData", RF_ServiceData)
)

def make_data_packet(pkt):
    return pkt + '\0'*(32 - len(pkt) - 1) + chr(len(pkt))
