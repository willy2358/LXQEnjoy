from GameStages.GameStage import GameStage


class PlayCards(GameStage):
    def __init__(self, rule):
        super(PlayCards, self).__init__(rule)
        self.__player_idx_of_play_card = -1
        self.__ordered_players = None
    def is_completed(self):
        return False

    def begin(self):
        rule = self.get_my_rule()
        round = self.get_my_round()
        self.__ordered_players = rule.order_play_card_players(round)
