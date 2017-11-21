
from GameStages.GameStage import GameStage

import random


class RandomBanker(GameStage):
    def __init__(self, rule):
        super(RandomBanker, self).__init__(rule)

    @staticmethod
    def execute(game_round):
        players = game_round.get_players()
        idx = random.randint(0, len(players) - 1)
        banker = players[idx]
        game_round.set_bank_player(banker)

    @staticmethod
    def is_ended_in_round(game_round):
        banker = game_round.get_bank_player()
        if not banker:
            return False
        else:
            return True

