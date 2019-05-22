#!/usr/bin/env python

import xml.etree.ElementTree as ET
from txt_colors import txt

set_staff_start_cb = None
set_staff_end_cb = None
set_time_signature_cb = None
set_pitch_cb = None
set_rest_cb = None
set_lyric_cb = None
set_tie_cb = None
set_dot_cb = None

SET_TAB = txt.TAB * 30

def set_time_signature(n, d):
    print(SET_TAB + txt.CRED + "set_time_signature" + txt.CEND, n, d)
    global set_time_signature_cb
    if set_time_signature_cb:
        set_time_signature_cb(n, d)

def parse_time_signature(v):
    n = d = ""
    for t in v.findall("./"):
        print(txt.TAB * 4, txt.CBEIGE + t.tag + txt.CEND, [t.attrib, t.tail.strip(), t.text.strip()])
        if (t.tag == "sigN"):
            n = t.text
        elif (t.tag == "sigD"):
            d = t.text
    set_time_signature(n, d)

def set_pitch(pitch, duration):
    print(SET_TAB + txt.CRED + "set_pitch" + txt.CEND, pitch, duration)
    global set_pitch_cb
    if set_pitch_cb:
        set_pitch_cb(pitch, duration)

def set_lyric(lyric):
    print(SET_TAB + txt.CRED + "set_lyric" + txt.CEND, lyric)
    global set_lyric_cb
    if set_lyric_cb:
        set_lyric_cb(lyric)

def set_tie():
    print(SET_TAB + txt.CRED + "set_tie" + txt.CEND)
    global set_tie_cb
    if (set_tie_cb):
        set_tie_cb()

def set_dot(num):
    print(SET_TAB + txt.CRED + "set_dot" + txt.CEND, num)
    global set_dot_cb
    if (set_dot_cb):
        set_dot_cb(num)

def parse_chord(v):
    duration = ""
    for c in v.findall("./"):
        print(txt.TAB * 4, txt.CBEIGE + c.tag + txt.CEND, [c.attrib, c.tail.strip(), c.text.strip()])
        if (c.tag == "durationType"):
            duration = c.text
        elif (c.tag == "dots"):
            set_dot(c.text)
        elif (c.tag == "Lyrics"):
            for l in c.findall("./"):
                print(txt.TAB * 5, txt.CRED2 + l.tag + txt.CEND, [l.attrib, l.tail.strip(), str(l.text).strip()])
                if (l.tag == "text" and l.text != None):
                    set_lyric(l.text)
        elif (c.tag == "Note"):
            for n in c.findall("./"):
                print(txt.TAB * 5, txt.CRED2 + n.tag + txt.CEND, [n.attrib, n.tail.strip(), n.text.strip()])
                if (n.tag == "Spanner" and n.attrib['type'] == "Tie"):
                    for s in n.findall("./"):
                        print(txt.TAB * 6, s.tag, [s.attrib, s.tail.strip(), s.text.strip()])
                        if (s.tag == "next"):
                            set_tie()
                elif (n.tag == "pitch"):
                    set_pitch(n.text, duration)

def set_rest(duration):
    print(SET_TAB + txt.CRED + "set_rest" + txt.CEND, duration)
    global set_rest_cb
    if set_rest_cb:
        set_rest_cb(duration)

def parse_rest(v):
    for r in v.findall("./"):
        print(txt.TAB * 4, txt.CBEIGE + r.tag + txt.CEND, [r.attrib, r.tail.strip(), r.text.strip()])
        if (r.tag == "durationType"):
            set_rest(r.text)

def parse_root(r):
    for s in r.findall("./Score/Staff"):
        print(txt.CBLUE + s.tag + txt.CEND, [s.attrib, s.tail.strip(), s.text.strip()])
        m_count = 0
        global set_staff_start_cb
        if (set_staff_start_cb):
            set_staff_start_cb()
        for m in s.findall("./"):
            print(txt.TAB * 1, txt.CGREEN + m.tag + txt.CEND, m_count, [m.attrib, m.tail.strip(), m.text.strip()])
            if (m.tag == "Measure"):
                m_count += 1
                for w in m.findall("./"):
                    print(txt.TAB * 2, txt.CVIOLET + w.tag + txt.CEND, [w.attrib, w.tail.strip(), w.text.strip()])
                    if (w.tag == "voice"):
                        for v in w.findall("./"):
                            print(txt.TAB * 3, txt.CYELLOW + v.tag + txt.CEND, [v.attrib, v.tail.strip(), v.text.strip()])
                            if (v.tag == "TimeSig"):
                                parse_time_signature(v)
                            elif (v.tag == "Chord"):
                                parse_chord(v)
                            elif (v.tag == "Rest"):
                                parse_rest(v)
        global set_staff_end_cb
        if (set_staff_end_cb):
            set_staff_end_cb()
        break

def parse_xml(xml_file, set_staff_start_func = None, set_staff_end_func = None, set_time_signature_func = None,
                set_pitch_func = None, set_rest_func = None, set_lyric_func = None, set_tie_func = None, set_dot_func = None):
    if (set_staff_start_func):
        global set_staff_start_cb
        set_staff_start_cb = set_staff_start_func
    if (set_staff_end_func):
        global set_staff_end_cb
        set_staff_end_cb = set_staff_end_func
    if (set_time_signature_func):
        global set_time_signature_cb
        set_time_signature_cb = set_time_signature_func
    if (set_pitch_func):
        global set_pitch_cb
        set_pitch_cb = set_pitch_func
    if (set_rest_func):
        global set_rest_cb
        set_rest_cb = set_rest_func
    if (set_lyric_func):
        global set_lyric_cb
        set_lyric_cb = set_lyric_func
    if (set_tie_func):
        global set_tie_cb
        set_tie_cb = set_tie_func
    if (set_dot_func):
        global set_dot_cb
        set_dot_cb = set_dot_func

    tree = ET.parse(xml_file)
    root = tree.getroot()
    parse_root(root)
    return(root)