#!/usr/bin/env python

import utils.common

#   <Rest>
#     <durationType>measure</durationType>
#     <duration>4/4</duration>
#     </Rest>

'''/museScore/Score/Staff/Measure/voice/Rest'''
'''/museScore/Score/Staff/Measure/voice/Rest/durationType'''
'''/museScore/Score/Staff/Measure/voice/Rest/duration'''

durationType = {
    "quarter": "QUARTER",
    "eighth":  "EIGHTH",
    "1024th":  "1024TH",
    "512th":   "512TH",
    "256th":   "256TH",
    "128th":   "128TH",
    "64th":    "64TH",
    "32nd":    "32ND",
    "16th":    "16TH",
    "half":    "HALF",
    "whole":   "WHOLE",
    "measure": "MEASURE",
    "breve":   "BREVE",
    "long":    "LONG"
}

def get_elements_from_rest(rest):
    return rest.findall("./*")

def handle_elements(element):
    if (element.tag == "durationType"):
        print(durationType[element.text])
    elif (element.tag == "duration"):
        print(element.text)
    else:
        print(utils.common.dbg(), element.tag, "not implemented")

def parse(rest):
    print(rest.tag)
    elements = get_elements_from_rest(rest)
    for e in elements:
        handle_elements(e)
