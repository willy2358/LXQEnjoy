from GameRules.Condition import Condition


class Condition_OneOption(Condition):
    def __init__(self):
        self.__options = []

    def add_option(self, option):
        self.__options.append(option)

