
CONDITION_PROPERTY_PLAYER_COUNT = 1
CONDITION_PROPERTY_TIME_OUT = 2
CONDITION_CARDS_DEAL_RESPONSE = 3


class GameStage:
    def __init__(self, name):
        self.__name = name
        self.__complete_conditions = []
        self.__abort_conditions = []

    def get_name(self):
        return self.__name

    def add_complete_condition(self, prop, value):
        self.__complete_conditions.append((prop, value))

    def add_abort_condition(self, prop, value):
        self.__abort_conditions.append((prop, value))




