
from GameRules.CardsPattern import CardsPattern

class CardsPattern_Majiang(CardsPattern):
    def __init__(self, name, score = 0):
        super(CardsPattern_Majiang, self).__init__(name, score)
        self.__conditions = []

    def add_condition(self, condition):
        self.__conditions.append(condition)
