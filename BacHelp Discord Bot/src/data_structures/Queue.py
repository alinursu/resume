
class Queue():
    __queue = []
    __queueSize = 0

    def __init__(self):
        self.__queue_= []
        self.__queueSize = 0

    def push(self, item):
        for qItem in self.__queue:
            if qItem == item:
                return

        self.__queue.append(item)
        self.__queueSize = self.__queueSize + 1

    def pop(self):
        if self.__queueSize == 0:
            return None

        temp = self.__queue.pop(0)
        self.__queueSize = self.__queueSize - 1
        return temp