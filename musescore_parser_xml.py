#!/usr/bin/env python

import utils.common

import xml.etree.ElementTree as ET
import musescore_handlers.musescore_keysig_handler as keysig_handler
import musescore_handlers.musescore_timesig_handler as timesig_handler
import musescore_handlers.musescore_tempo_handler as tempo_handler
import musescore_handlers.musescore_chord_handler as chord_handler
import musescore_handlers.musescore_rest_handler as rest_handler

def read_xml_tree_from_file(file_name):
    xml_tree = ET.parse(file_name)
    return xml_tree

def read_xml_root_from_string(xml_string):
    root = ET.fromstring(xml_string)
    return root

def get_xml_root_from_xml_tree(xml_tree):
    return xml_tree.getroot()

def print_all(tag, tab):
    print(tab + tag.tag, tag.attrib, tag.text)
    tab += "  "
    for child in tag:
        print_all(child, tab)

def write_xml_tree_to_file(xml_tree, file_name):
    xml_tree.write(file_name)

def get_part_staff_ids():
    ids = [staff.attrib['id'] for staff in root.findall("./Score/Part/Staff[@id]")]
    return ids

def get_part_staff_by_id(id):
    try:
        return root.findall("./Score/Part/Staff[@id='" + id + "']")[0]
    except:
        None

def get_staff_by_id(id):
    try:
        return root.findall("./Score/Staff[@id='" + id + "']")[0]
    except:
        None

def get_measures_from_staff(staff):
    '''/museScore/Score/Staff/Measure'''
    return staff.findall("./Measure")

def get_voices_from_measure(measure):
    '''/museScore/Score/Staff/Measure/voice'''
    return measure.findall("./voice")

def get_elements_from_voice(voice):
    '''/museScore/Score/Staff/Measure/voice/*'''
    '''/museScore/Score/Staff/Measure/voice/KeySig'''
    '''/museScore/Score/Staff/Measure/voice/TimeSig'''
    '''/museScore/Score/Staff/Measure/voice/Tempo'''
    '''/museScore/Score/Staff/Measure/voice/Chord'''
    '''/museScore/Score/Staff/Measure/voice/Rest'''
    return voice.findall("./*")

def handle_voice_element(element):
    if (element.tag == "KeySig"):
        keysig_handler.parse(element)
    elif (element.tag == "TimeSig"):
        timesig_handler.parse(element)
    elif (element.tag == "Tempo"):
        tempo_handler.parse(element)
    elif (element.tag == "Chord"):
        chord_handler.parse(element)
    elif (element.tag == "Rest"):
        rest_handler.parse(element)
    else:
        print(utils.common.dbg(), e.tag, "not implemented")

if __name__ == "__main__":
    tree = read_xml_tree_from_file("./tests/xml/test_title.mscx")
    root = get_xml_root_from_xml_tree(tree)
    staff = get_staff_by_id('1')
    measures = get_measures_from_staff(staff)
    for i,m in enumerate(measures):
        print("BAR:", i)
        voices = get_voices_from_measure(m)
        for v in voices:
            elements = get_elements_from_voice(v)
            for e in elements:
                handle_voice_element(e)

    # write_xml_tree_to_file(tree, "./tests/xml/test_title_copy.mscx")