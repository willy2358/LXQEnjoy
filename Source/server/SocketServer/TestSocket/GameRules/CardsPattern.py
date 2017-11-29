
class CardsPattern:
    def __init__(self, name, score = 0):
        self.__power = score  # 1 has the lowest power, 2, is more, 3, is more than 2,
        self.__name = name
        self.__score = score

    def get_score(self):
        return self.__score

    def get_power(self):
        return self.__power

    def set_power(self, power):
        self.__power = power

    def set_score(self, score):
        self.__score = score

