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

if __name__ == "__main__":
    tree = read_xml_tree_from_file("./tests/xml/basic.xml")
    root = get_xml_root_from_xml_tree(tree)
    write_xml_tree_to_file(tree, "./tests/xml/basic_copy.xml")