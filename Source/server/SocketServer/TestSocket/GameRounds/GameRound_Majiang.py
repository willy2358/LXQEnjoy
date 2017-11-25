
from GameRounds.GameRound import GameRound
import InterProtocol
import PlayCmd

class GameRound_Majiang(GameRound):
    def __init__(self, rule):
        super(GameRound_Majiang, self).__init__(rule)

        self.__one_play_starter = None

    def set_one_play_starter(self, player):
        self.__one_play_starter = player

    def get_cur_play_starter(self):
        return self.__one_play_starter

    def get_one_play_listeners(self, starter):
        idx = self._players.index(starter)
        listeners = self._players[idx + 1:] + self._players[:idx]
        return listeners

    def player_select_peng(self, player, card):
        self.reset_player_waiting_for_cmd_resp()
        player.move_cards_to_freeze_group([card, card], [card])


    def player_select_gang(self, player, card):
        self.reset_player_waiting_for_cmd_resp()
        player.move_cards_to_freeze_group([card, card, card], [card])

