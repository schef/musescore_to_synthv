#!/usr/bin/env python

import xml.etree.ElementTree as ET

class txt:
    ENDC = '\033[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    TAB = '  '

durationType = {
    'measure' : 1, #TODO: match bar
    'whole' : 1,
    'half' : 2,
    'quarter' : 4,
    'eighth' : 8,
    '16th' : 16,
    '32nd' : 32
}

tree = ET.parse('examples/musicxml.mscx')
root = tree.getroot()

staff = []

for s in root.findall("./Score/Staff"):
    staff.append(s)

for s in staff:
    print("Staff", s.attrib)
    m_count = 0
    for m in s.findall("./Measure"):
        print(txt.TAB, m.tag, m_count)
        m_count += 1
        for v in m.findall("./voice/*"):
            print(txt.TAB * 2, v.tag)
            if (v.tag == "Chord"):
                duration = 0
                for c in v.findall("./*"):
                    print(txt.TAB * 3, c.tag)
                    if (c.tag == "durationType"):
                        duration = durationType[c.text]
                    if (c.tag == "Note"):
                        for n in c.findall("./*"):
                            if (n.tag == "pitch"):
                                print(txt.TAB * 4, n.text, duration)
            elif (v.tag == "Rest"):
                for r in v.findall("./*"):
                    print(txt.TAB * 3, r.tag)
                    duration = 0
                    if (r.tag == "durationType"):
                        duration = durationType[r.text]
                        print(txt.TAB * 4, "r" + str(duration))
