#!/usr/bin/env python

import xml.etree.ElementTree as ET

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
    return staff.findall("./Measure")

if __name__ == "__main__":
    tree = read_xml_tree_from_file("./tests/xml/test_title.mscx")
    root = get_xml_root_from_xml_tree(tree)
    # write_xml_tree_to_file(tree, "./tests/xml/test_title_copy.mscx")