

class PlayRule:
    def __init__(self, rule_id):
        self.__player_num_min = 0;
        self.__player_num_max = 0;
        # 设置底牌数
        self.__cards_num_not_deal = 0;
        self.__rule_id = rule_id;
        self.__cards = []

    def set_player_min_number(self, number):
        self.__player_num_min = number

    def set_player_mzx_number(self, number):
        self.__player_num_max = number

    def set_cards_number_not_deal(self, number):
        self.__cards_num_not_deal = number

    def get_cards_number_not_deal(self):
        return self.__cards_num_not_deal

    def set_cards(self, cards):
        self.__cards = cards

    def get_player_min_number(self):
        return self.__player_num_min

    def get_play_rule_id(self):
        return self.__rule_id

    def get_cards(self):
        return self.__cards


