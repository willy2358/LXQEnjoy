from GameStages.CalScores import CalScores
import CardsMaster
from GameRules.WinTester_Majiang import WinTester_Majiang

class CalScores_Majiang(CalScores):
    def __init__(self, rule):
        super(CalScores_Majiang, self).__init__(rule)

    @staticmethod
    def execute(game_round):
        winner = game_round.get_winners()[0]
        cards = winner.get_in_hand_cards()
        rule = game_round.get_rule()
        pattern = "pi hu"
        score = game_round.get_pattern_default_score()
        win_patterns = rule.get_win_patterns()
        for p in win_patterns:
            if p.is_match(cards):
                score = p.get_score()
                pattern = p.get_name()

        is_zimo = winner.get_final_cards_is_from_dealer()
        test_cards = cards.remove(winner.get_final_cards())
        wan_s = CardsMaster.def_wans["wan-1"]
        suo_s = CardsMaster.def_suos["suo-1"]
        ton_s = CardsMaster.def_tons["ton-1"]

        only_one_win_card = True
        testee = [c for c in range(wan_s, wan_s + 9)]  + [c for c in range(suo_s, suo_s + 9)] \
                 + [c for c in range(ton_s, ton_s + 9)]
        for c in testee:
            if WinTester_Majiang.is_card_win_for_cards(c, test_cards):
                only_one_win_card = False
                break

        final_score = 10
        winner.set_won_score(final_score)
        for l in game_round.get_losers():
            l.set_won_score(-final_score)


    @staticmethod
    def is_ended_in_round(game_round):
        for w in game_round.get_winners():
            if w.get_won_score() > 0:
                return True
