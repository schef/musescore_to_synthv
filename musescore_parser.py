#!/usr/bin/env python

import xml.etree.ElementTree as ET
from txt_colors import txt

set_staff_start_cb = None
set_staff_end_cb = None
set_time_signature_cb = None
set_pitch_cb = None
set_rest_cb = None

def set_time_signature(n, d):
    # print(txt.CRED + "set_time_signature" + txt.CEND, n, d)
    global set_time_signature_cb
    if set_time_signature_cb:
        set_time_signature_cb(n, d)

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
    # print(txt.CRED + "set_pitch" + txt.CEND, pitch, duration)
    global set_pitch_cb
    if set_pitch_cb:
        set_pitch_cb(pitch, duration)

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
    # print(txt.CRED + "set_rest" + txt.CEND, duration)
    global set_rest_cb
    if set_rest_cb:
        set_rest_cb(duration)

def parse_rest(v):
    for r in v.findall("./*"):
        print(txt.TAB * 3, r.tag)
        if (r.tag == "durationType"):
            set_rest(r.text)

def parse_root(r):
    for s in r.findall("./Score/Staff"):
        print("Staff", s.attrib)
        m_count = 0
        global set_staff_start_cb
        if (set_staff_start_cb):
            set_staff_start_cb()
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
        global set_staff_end_cb
        if (set_staff_end_cb):
            set_staff_end_cb()

def parse_xml(xml_file, set_staff_start_func = None, set_staff_end_func = None, set_time_signature_func = None, set_pitch_func = None, set_rest_func = None):
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

    tree = ET.parse(xml_file)
    root = tree.getroot()
    parse_root(root)