
from GameStages import GameStage


class DealMaJiangs(GameStage):

    def __init__(self):
        pass

    @staticmethod
    def execute(game_round):
        rule = game_round.get_rule()
        banker_cards_num = rule.get_cards_number_for_banker()
        player_cards_num = rule.get_cards_number_for_non_banker()
        for p in game_round.get_players():
            if p.is_banker():
                game_round.deal_cards_for_player(p, banker_cards_num)
            else:
                game_round.deal_cards_for_player(p, player_cards_num)

    @staticmethod
    def is_ended_in_round(game_round):
        rule = game_round.get_rule()
        banker_cards_num = rule.get_cards_number_for_banker()
        player_cards_num = rule.get_cards_number_for_non_banker()
        for p in game_round.get_players():
            init_cards_num = len(p.get_init_cards())
            if p.is_banker() and init_cards_num < banker_cards_num:
                return False
            if not p.is_banker() and init_cards_num < player_cards_num:
                return False

        return True


