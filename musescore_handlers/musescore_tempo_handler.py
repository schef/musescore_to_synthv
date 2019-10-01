#!/usr/bin/env python

#   <Tempo>
#     <tempo>1.65</tempo>
#     <followText>1</followText>
#     <text><sym>metNoteQuarterUp</sym> = 99</text>
#     </Tempo>

'''/museScore/Score/Staff/Measure/voice/Tempo'''
'''/museScore/Score/Staff/Measure/voice/Tempo/tempo'''
'''/museScore/Score/Staff/Measure/voice/Tempo/followText'''
'''/museScore/Score/Staff/Measure/voice/Tempo/text'''
'''/museScore/Score/Staff/Measure/voice/Tempo/text/sym'''

def get_elements_from_tempo(tempo):
    return tempo.findall("./*")

def handle_elements(element):
    if (element.tag == "tempo"):
        print(element.text)
    else:
        print(__file__, element.tag, "not implemented")

def parse(tempo):
    print(tempo.tag)
    elements = get_elements_from_tempo(tempo)
    for e in elements:
        handle_elements(e)