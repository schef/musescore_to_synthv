class ProgramRevision():
    def __init__(self, element):
        self.__element = element

    def getRevision(self):
        return self.__element.text
