from GCore.Statement import Statement

class Delay(Statement):
    def __init__(self, seconds):
        self.__seconds = seconds
        