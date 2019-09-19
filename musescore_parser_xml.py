#!/usr/bin/env python

import xml.etree.ElementTree as ET

def read_xml_root_from_file(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    return root

def read_xml_root_from_string(xml_string):
    root = ET.fromstring(xml_string)
    return root

def print_all(tag, tab):
    print(tab + tag.tag, tag.attrib, tag.text)
    tab += "  "
    for child in tag:
        print_all(child, tab)


if __name__ == "__main__":
    root = read_xml_root_from_file("./tests/xml/basic.xml")
    print_all(root, "")