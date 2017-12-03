

class WinTester_Majiang:
    def __init__(self, default_score = 1):
        pass

    @staticmethod
    def is_card_win_for_cards(card, cards):
        if cards.count(card) >=  1:
            return WinTester_Majiang.can_cards_win(cards + [card])
        if card + 1 in cards and card + 2 in cards:
            return WinTester_Majiang.can_cards_win(cards + [card])
        if card - 2 in cards and card - 1 in cards:
            return WinTester_Majiang.can_cards_win(cards + [card])
        if card - 1 in cards and card + 1 in cards:
            return WinTester_Majiang.can_cards_win(cards + [card])
        return False

    @staticmethod
    def can_cards_win(cards):
        if WinTester_Majiang.__get_pair_count(cards) == len(cards) / 2 and len(cards) % 2 == 0:  # 7 pairs
            return True
        jiang_opts = WinTester_Majiang.__get_jiang_options(cards)  # jiang is a must
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
            if WinTester_Majiang.__are_cards_all_grouped(wans_2) \
                    and WinTester_Majiang.__are_cards_all_grouped(suos_2) \
                    and WinTester_Majiang.__are_cards_all_grouped(tons_2):
                return True

        return False

    @staticmethod
    def __are_cards_all_grouped(cards):
        lefts = WinTester_Majiang.__get_forward_bad_cards(cards)
        if WinTester_Majiang.__get_single_count(lefts) > 0 or WinTester_Majiang.__get_pair_count(lefts) > 0:
            return False
        else:
            return True

    @staticmethod
    def __get_jiang_options(cards):
        opts = []
        for c in cards:
            if cards.count(c) >= 2 and c not in opts:
                opts.append(c)
        return opts

    @staticmethod
    def __get_forward_bad_cards(cards):
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
    def __get_single_count(cards):
        # uniq = set(cards)
        uniqs = [x for x in cards if cards.count(x) == 1]
        return len(uniqs)

    @staticmethod
    def __get_pair_count(cards):
        dual = set([x for x in cards if cards.count(x) == 2])
        return len(dual)
