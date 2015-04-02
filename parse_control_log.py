#!/usr/bin/env python

import sys
import re
import fbpacket

reg = re.compile(r'CONTROL (?P<direction>IN|OUT) bytes: (?P<data>[A-F0-9]+)')

with open(sys.argv[1]) as logfile:
    for line in logfile:
        match = reg.search(line)
        if match:
            res = match.groupdict()
            if res['direction'] == 'IN':
                print "<== %s" % res['data']
                print fbpacket.parse_hid_IN(res['data'].decode('hex'))
            elif res['direction'] == 'OUT':
                print "==> %s" % res['data']
                print fbpacket.parse_hid_OUT(res['data'].decode('hex'))
