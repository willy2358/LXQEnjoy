
from Cards.GType import *

class Pattern:
    ATTR_NAME_POWER = "power"
    def __init__(self, gRule = GType.Poker):
        self.__power = 0
        self.__power_statements = []
        self.__leading = True
        self.__leading_statements = []
        self.__gRule = gRule
        self.__name = "unknown"
        self.__effect ="undefined"#just a text, user can customize against the text.

    def get_power(self):
        return self.__power

    def set_power(self, power):
        self.__power = power

    def add_power_statement(self, clause):
        self.__power_statements.append(clause)

    def add_leading_statement(self, clause):
        self.__leading_statements.append(clause)

    def get_leading(self):
        return self.__leading

    def is_my_pattern(self, cards):
        pass

    def getGRule(self):
        return self.__gRule

    @staticmethod
    def calculate_power(cards):
        return 0

    @staticmethod
    def calculate_leading(cards):
        return False
