from GameRules.GameRule import GameRule


class GameRule_Majiang(GameRule):
    def __init__(self, rule_id):
        super(GameRule_Majiang, self).__init__(rule_id)
        self.__banker_cards_number = 14
        self.__non_banker_cards_number = 13

    def is_player_win(self, player):
        pass

    def get_cards_number_for_banker(self):
        return self.__banker_cards_number

    def get_cards_number_for_non_banker(self):
        return self.__nonbanker_cards_number

    def set_cards_number_for_banker(self, number):
        self.__banker_cards_number = number

    def set_cards_number_for_non_banker(self, number):
        self.__non_banker_cards_number = number

    def get_cmd_options_for_cards(self, cards):
        pass

    def get_first_cards_player(self, players):
        for p in players:
            if p.is_banker:
                return p
