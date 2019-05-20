#!/usr/bin/env python

from txt_colors import txt
import musescore_parser as MP


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

def set_pitch(pitch, duration):
    print(txt.CRED + "set_pitch" + txt.CEND, pitch, duration)    

def set_rest(duration):
    print(txt.CRED + "set_rest" + txt.CEND, duration)

MP.parse_xml('examples/musicxml.mscx', set_time_signature, set_pitch, set_rest)