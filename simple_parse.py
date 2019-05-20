#!/usr/bin/env python

import xml.etree.ElementTree as ET

class txt:
    CEND = '\033[0m'
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

time_signature_n = 0
time_signature_d = 0

def get_time_signature_duration(n, d):
    if (n == 4 and n == 4):
        return 1
    elif (n == 3 and n == 4):
        return duration_type[whole]
    elif (n == 6 and n == 8):
        return duration_type[whole]

duration_type = {
    'measure' : get_time_signature_duration(time_signature_n, time_signature_d),
    'whole' : 1,
    'half' : 2,
    'quarter' : 4,
    'eighth' : 8,
    '16th' : 16,
    '32nd' : 32
}

def set_time_signature(n, d):
    print(txt.CRED + "set_time_signature" + txt.CEND, n, d)

def parse_time_signature(v):
    n = d = ""
    for t in v.findall("./*"):
        print(txt.TAB * 3, t.tag)
        if (t.tag == "sigN"):
            n = t.text
        elif (t.tag == "sigD"):
            d = t.text
    set_time_signature(n, d)

def set_pitch(pitch, duration):
    print(txt.CRED + "set_pitch" + txt.CEND, pitch, duration)    

def parse_chord(v):
    duration = ""
    for c in v.findall("./*"):
        print(txt.TAB * 3, c.tag)
        if (c.tag == "durationType"):
            duration = c.text
        if (c.tag == "Note"):
            for n in c.findall("./*"):
                if (n.tag == "pitch"):
                    set_pitch(n.text, duration)

def set_rest(duration):
    print(txt.CRED + "set_rest" + txt.CEND, duration)

def parse_rest(v):
    for r in v.findall("./*"):
        print(txt.TAB * 3, r.tag)
        if (r.tag == "durationType"):
            set_rest(r.text)

def parse_root(r):
    for s in r.findall("./Score/Staff"):
        print("Staff", s.attrib)
        m_count = 0
        for m in s.findall("./Measure"):
            print(txt.TAB, m.tag, m_count)
            m_count += 1
            for v in m.findall("./voice/*"):
                print(txt.TAB * 2, v.tag)
                if (v.tag == "TimeSig"):
                    parse_time_signature(v)
                elif (v.tag == "Chord"):
                    parse_chord(v)
                elif (v.tag == "Rest"):
                    parse_rest(v)

tree = ET.parse('examples/musicxml.mscx')
root = tree.getroot()
parse_root(root)