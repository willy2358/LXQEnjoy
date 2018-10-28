from GCore.Statement import Statement

#sleep for some seconds
class Delay(Statement):
    def __init__(self, seconds):
        self.__seconds = seconds
