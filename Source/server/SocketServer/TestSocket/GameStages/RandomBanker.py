
from GameStages.GameStage import GameStage

import random


class RandomBanker(GameStage):
    def __init__(self, rule):
        super(RandomBanker, self).__init__(rule)

    @staticmethod
    def execute(game_round):
        players = game_round.get_players()
        idx = random.randint(0, len(players))
        banker = players[idx]
        game_round.set_bank_player(banker)
