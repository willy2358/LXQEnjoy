
from GameRules.CardsPattern import CardsPattern

class CardsPattern_Majiang(CardsPattern):
    def __init__(self):
        super(CardsPattern_Majiang, self).__init__()
        self.__conditions = []
        self.__score = 10

    def set_score(self, score):
        self.__score = score

    def add_condition(self, condition):
        self.__conditions.append(condition)
