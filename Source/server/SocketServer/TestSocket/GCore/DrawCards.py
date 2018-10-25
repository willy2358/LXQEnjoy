
from GCore.Statement import Statement

class DrawCards(Statement):
    def __init__(self, var, count):
        self.__var = var
        self.__count = count

    