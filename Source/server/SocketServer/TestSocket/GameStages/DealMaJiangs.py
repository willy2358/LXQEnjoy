
from GameStages.GameStage import GameStage


class DealMaJiangs(GameStage):

    def __init__(self, rule):
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
            game_round.publish_player_cards_update(p)

    @staticmethod
    def is_ended_in_round(game_round):
        rule = game_round.get_rule()
        banker_cards_num = rule.get_cards_number_for_banker()
        player_cards_num = rule.get_cards_number_for_non_banker()
        for p in game_round.get_players():
            cards_num = len(p.get_in_hand_cards())
            if p.is_banker() and cards_num < banker_cards_num:
                return False
            if not p.is_banker() and cards_num < player_cards_num:
                return False

        return True


