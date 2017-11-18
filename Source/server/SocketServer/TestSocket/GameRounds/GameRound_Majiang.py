
from GameRounds.GameRound import GameRound

# terms: one-play: includes:
# letting one player play one card, this play is called the starter
# this player played one card
# letting other players response to the played card, these players are called listeners
# one listener got the played card or got a new card from table
# this listener become the starter of new one-play, new one-play begins


class GameRound_Majiang(GameRound):
    def __init__(self, rule):
        super(GameRound_Majiang, self).__init__(rule)

        self.__one_play_starter = None

    def set_one_play_starter(self, player):
        self.__one_play_starter = player

    def get_cur_play_starter(self):
        return self.__one_play_starter

    def get_one_play_listeners(self, starter):
        idx = self.__players.index(starter)
        listeners = self.__players[idx + 1:] +  self.__players[:idx]
        return listeners

    def player_select_peng(self, player, card):
        pass

    def player_select_gang(self, player, card):
        pass

    # def test_and_update_current_stage(self):
    #     if not self.get_cur_game_stage():
    #         stage = self.get_next_game_stage()
    #         self.set_cur_game_stage(stage)
    #
    #     cur_stage = self.get_cur_game_stage()
    #     if cur_stage:
    #         if cur_stage.is_ended_in_round(self):
    #             cur_stage = self.get_next_game_stage()
    #
    #     if cur_stage:
    #         cur_stage.execute(self)
