#!/usr/bin/env python3

from inspect import currentframe, getframeinfo
import inspect
import xml.etree.ElementTree as ET

class txt:
    CEND = '\033[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    CTAB = '  '

def dbg():
    file_name = inspect.stack()[1][1]
    line_num = inspect.stack()[1][2]
    func_name = inspect.stack()[1][3]
    string = ""
    string += "["
    string += txt.CBOLD + txt.CYELLOW
    string += file_name.split('/')[-1]
    string += txt.CEND
    string += ":"
    string += txt.CBOLD + txt.CBLUE
    string += str(line_num)
    string += txt.CEND
    string += "]"
    return(string)

class XmlParser:
    def read_xml_tree_from_file(file_name):
        xml_tree = ET.parse(file_name)
        return xml_tree

    def write_xml_tree_to_file(xml_tree, file_name):
        xml_tree.write(file_name)

    def get_xml_root_from_xml_tree(xml_tree):
        return xml_tree.getroot()

    def get_child_by_tag(element, tag):
        for child in list(element):
            if child.tag == tag:
                return child
        return None
    
    def get_children_by_tag(element, tag):
        children = []
        for child in list(element):
            if child.tag == tag:
                children.append(child)
        return children