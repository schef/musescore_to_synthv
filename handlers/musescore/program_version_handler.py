class ProgramVersion():
    def __init__(self, element):
        self.__element = element

    def getVersion(self):
        return self.__element.text
