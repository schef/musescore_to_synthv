from utils.common import *
from handlers.musescore.score.division_handler import *
from handlers.musescore.score.staff_handler import *

class Score():
    def __init__(self, element):
        self.__element = element
        self.division = Division(XmlParser.get_child_by_tag(self.__element, 'Division'))
        self.staff = []
        for s in XmlParser.get_children_by_tag(self.__element, 'Staff'):
            self.staff.append(Staff(s))