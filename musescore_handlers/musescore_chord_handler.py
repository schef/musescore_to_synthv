#!/usr/bin/env python

'''/museScore/Score/Staff/Measure/voice/Chord'''
'''/museScore/Score/Staff/Measure/voice/Chord/durationType'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/pitch'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/tpc'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Accidental'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Accidental/role'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Accidental/subtype'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Spanner'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Spanner/Tie'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Spanner/Slur'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Spanner/next'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Spanner/next/location'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Spanner/next/location/fraction'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Spanner/prev'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Spanner/prev/location'''
'''/museScore/Score/Staff/Measure/voice/Chord/Note/Spanner/prev/location/fraction'''

def get_elements_from_chord(chord):
    return chord.findall("./*")

def handle_accidental_element(element):
    if (element.tag == "role"):
        print(element.text)
    elif (element.tag == "subtype"):
        print(element.text)
    else:
        print(__file__, element.tag, "not implemented")

def handle_spanner_next_fraction_element(element):
    if (element.tag == "fraction"):
        print(element.text)
    else:
        print(__file__, element.tag, "not implemented")

def handle_spanner_next_element(element):
    if (element.tag == "location"):
        handle_spanner_next_fraction_element(element)
    else:
        print(__file__, element.tag, "not implemented")
    
def handle_spanner_prev_fraction_element(element):
    if (element.tag == "fraction"):
        print(element.text)
    else:
        print(__file__, element.tag, "not implemented")

def handle_spanner_prev_element(element):
    if (element.tag == "location"):
        handle_spanner_prev_fraction_element(element)
    else:
        print(__file__, element.tag, "not implemented")  

def handle_spanner_element(element):
    if (element.tag == "Tie"):
        print(element.text)
    elif (element.tag == "Slur"):
        print(element.text)
    elif (element.tag == "next"):
        handle_spanner_next_element(element)
    elif (element.tag == "prev"):
        handle_spanner_prev_element(element)
    else:
        print(__file__, element.tag, "not implemented")

def handle_note_element(element):
    if (element.tag == "pitch"):
        print(element.text)
    elif (element.tag == "tpc"):
        print(element.text)
    elif (element.tag == "Accidental"):
        handle_accidental_element(element)
    elif (element.tag == "Spanner"):
        handle_spanner_element(element)
    else:
        print(__file__, element.tag, "not implemented")

def handle_element(element):
    if (element.tag == "durationType"):
        print(element.text)
    elif (element.tag == "Note"):
        handle_note_element(element)
    else:
        print(__file__, element.tag, "not implemented")

def parse(chord):
    print(chord.tag)
    elements = get_elements_from_chord(chord)
    for e in elements:
        handle_element(e)