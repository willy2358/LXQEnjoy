from GameRules.GameRule import GameRule

import InterProtocol


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
        return self.__non_banker_cards_number

    def set_cards_number_for_banker(self, number):
        self.__banker_cards_number = number

    def set_cards_number_for_non_banker(self, number):
        self.__non_banker_cards_number = number

    @staticmethod
    def get_player_cmd_options_for_cards(player, new_cards, is_next_player = False, is_cards_from_other_player = True):
        cmd_opts = []
        cards = player.get_in_hand_cards() + new_cards
        if GameRule_Majiang.can_cards_hu(cards):
            if is_cards_from_other_player:
                cmd_opts.append(InterProtocol.majiang_player_act_hu)
            else:
                cmd_opts.append(InterProtocol.majiang_player_act_zimo)

            if len(new_cards) == 0: # banker initially zi mo
                pass
            else:
                if is_next_player:
                    cmd_opts.append(InterProtocol.majiang_player_act_new_card)
                else:
                    cmd_opts.append(InterProtocol.majiang_player_act_pass)
        else:
            num = cards.count(new_cards[0])
            if num >= 3:
                if is_next_player:
                    cmd_opts.append(InterProtocol.majiang_player_act_new_card)
                else:
                    cmd_opts.append(InterProtocol.majiang_player_act_pass)

                cmd_opts.append(InterProtocol.majiang_player_act_peng)

                if num == 4:
                    cmd_opts.append(InterProtocol.majiang_player_act_gang)

        return cmd_opts

    def get_first_cards_player(self, players):
        for p in players:
            if p.is_banker:
                return p

    @staticmethod
    def can_cards_hu(cards):
        return False
