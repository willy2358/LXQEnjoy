from GameRules.GameRule import GameRule

import InterProtocol
from PlayCmd import PlayCmd

from enum import Enum
from GameRules.WinTester_Majiang import WinTester_Majiang

class WinType(Enum):
    dian_pao = 1
    win_3_others = 2

class GameRule_Majiang(GameRule):
    def __init__(self, rule_id):
        super(GameRule_Majiang, self).__init__(rule_id)
        self.__banker_cards_number = 14
        self.__non_banker_cards_number = 13

        self.__max_card_types = 3
        self.__min_card_types = 1
        self.__main_type_min_cards_number = 8
        self.__allow_all_pairs = True
        self.__win_type = WinType.dian_pao
        self.__is_guo_shui_hu = False
        self.__versatile_cards = []
        self.__random_versatile_cards_count = 0


    def is_player_win(self, player):
        pass

    def get_cards_number_for_banker(self):
        return self.__banker_cards_number

    def get_cards_number_for_non_banker(self):
        return self.__non_banker_cards_number

    def set_cards_number_for_banker(self, number):
        self.__banker_cards_number = number

    def set_cards_number_for_non_banker(self, number):
        self.__non_banker_cards_number = number



    @staticmethod
    def get_player_cmd_options_for_cards(player, new_cards, is_next_player = False, is_cards_from_other_player = True):
        cmd_opts = []
        def_cmd = None
        cards = player.get_active_cards() + new_cards
        if WinTester_Majiang.can_cards_win(cards):
            if is_cards_from_other_player:
                cmd_opts.append(PlayCmd(player, InterProtocol.majiang_player_act_hu))
            else:
                cmd_opts.append(PlayCmd(player, InterProtocol.majiang_player_act_zimo))
        if new_cards and cards.count(new_cards[0]) == 3 and is_cards_from_other_player:
            cmd_opts.append(PlayCmd(player, InterProtocol.majiang_player_act_peng))
        # gang can be execute any time
        uniq_cards = set(cards)
        for c in uniq_cards:
            if cards.count(c) == 4:
                gang = PlayCmd(player, InterProtocol.majiang_player_act_gang)
                gang.set_cmd_param([c])
                cmd_opts.append(gang)

        return cmd_opts

