from utils.common import *
from handlers.musescore.program_version_handler import *
from handlers.musescore.program_revision_handler import *
from handlers.musescore.score_handler import *

class MuseScore():
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__tree = XmlParser.read_xml_tree_from_file(self.__file_name)
        self.__root = XmlParser.get_xml_root_from_xml_tree(self.__tree)
        self.programVersion = ProgramVersion(XmlParser.get_child_by_tag(self.__root, 'programVersion'))
        self.programRevision = ProgramRevision(XmlParser.get_child_by_tag(self.__root, 'programRevision'))
        self.score = Score(XmlParser.get_child_by_tag(self.__root, 'Score'))

    def getVersion(self):
        try:
            return self.__root.attrib['version']
        except:
            return None

    def setVersion(self, version):
        try:
            self.__root.attrib['version'] = version
        except:
            print("field 'version' does not exist")