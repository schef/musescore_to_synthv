from utils.common import *
from handlers.musescore.score.staff.vbox_handler import *

class Staff():
    def __init__(self, element):
        self.__element = element
        self.vbox = Vbox(XmlParser.get_child_by_tag(self.__element, 'Division'))

    def getId(self):
        try:
            return self.__element.attrib['id']
        except:
            return None
    
    def setId(self, id):
        self.__element.attrib['id'] = str(id)