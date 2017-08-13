from GameStages.GameStage import GameStage


class GroupPlayers(GameStage):
    def __init__(self, rule):
        super(GroupPlayers, self).__init__(rule)

    def is_completed(self):
        if self.get_my_round().get_players_count() == self.get_my_rule().get_player_min_number():
            return True

        return False

    def begin(self):
        pass
