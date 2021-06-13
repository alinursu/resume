
class Pair():
    __key = None
    __value = None

    def __init__(self, key, value):
        self.__key = key
        self.__value = value

    def getKey(self):
        return self.__key

    def getValue(self):
        return self.__value