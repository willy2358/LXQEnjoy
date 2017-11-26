from GameRules.GameRule import GameRule

import InterProtocol
from PlayCmd import PlayCmd


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
        def_cmd = None
        cards = player.get_active_cards() + new_cards
        if GameRule_Majiang.can_cards_hu(cards):
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

    # def get_first_cards_player(self, players):
    #     for p in players:
    #         if p.is_banker:
    #             return p

    @staticmethod
    def can_cards_hu(cards):
        if GameRule_Majiang.get_pair_count(cards) == len(cards) / 2 and len(cards) % 2 == 0:  # 7 pairs
            return True
        jiang_opts = GameRule_Majiang.get_jiang_options(cards) # jiang is a must
        if len(jiang_opts) < 1:
            return False

        wans = [c for c in cards if 10 < c < 20]
        suos = [c for c in cards if 20 < c < 30]
        tons = [c for c in cards if 30 < c < 40]
        for opt in jiang_opts:
            wans_2 = wans[:]
            suos_2 = suos[:]
            tons_2 = tons[:]
            if opt in wans_2:
                wans_2.remove(opt)
                wans_2.remove(opt)
            elif opt in suos_2:
                suos_2.remove(opt)
                suos_2.remove(opt)
            elif opt in tons_2:
                tons_2.remove(opt)
                tons_2.remove(opt)
            # the remained cards may be all gang or peng, this if test also honored this case
            if GameRule_Majiang.are_cards_all_grouped(wans_2) \
                    and GameRule_Majiang.are_cards_all_grouped(suos_2) \
                    and GameRule_Majiang.are_cards_all_grouped(tons_2):
                return True

        return False

    @staticmethod
    def are_cards_all_grouped(cards):
        lefts = GameRule_Majiang.get_forward_bad_cards(cards)
        if GameRule_Majiang.get_single_count(lefts) > 0 or GameRule_Majiang.get_pair_count(lefts) > 0:
            return False
        else:
            return True

    @staticmethod
    def get_jiang_options(cards):
        opts =[]
        for c in cards:
            if cards.count(c) >= 2 and c not in opts:
                opts.append(c)
        return opts

    @staticmethod
    def get_forward_bad_cards(cards):
        remainTests = cards[:]
        remainTests.sort()
        bads = []
        while remainTests and len(remainTests) > 0:
            head = remainTests[0]
            if (head + 1) in remainTests and (head + 2) in remainTests:
                remainTests.remove(head)
                remainTests.remove(head + 1)
                remainTests.remove(head + 2)
            else:
                remainTests.remove(head)
                bads.append(head)

        return bads

    @staticmethod
    def get_single_count(cards):
        # uniq = set(cards)
        uniqs = [x for x in cards if cards.count(x) == 1]
        return len(uniqs)

    @staticmethod
    def get_pair_count(cards):
        dual = set([x for x in cards if cards.count(x) == 2])
        return len(dual)
