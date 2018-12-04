
from GCore.Statement import Statement
import Mains.Log as Log

class PlayCards(Statement):
    def __init__(self, player, cards, act_alias, cards_face_up=True):
        super(PlayCards, self).__init__()
        self.__player = player
        self.__cards = cards
        self.__act_alias = act_alias
        self.__cards_face_up = cards_face_up


    def gen_runtime_obj(self, scene):
        def play_cards():
            try:
                player = scene.get_obj_value(self.__player)
                cards = scene.get_obj_value(self.__cards)
                if player and cards:
                    face_up = scene.get_obj_value(self.__cards_face_up)
                    cmd_args = cards
                    if not face_up:
                        cmd_args = ['*' for i in range(len(cards))]
                    scene.process_player_play_cards(player, cmd_args)

            except Exception as ex:
                Log.exception(ex)

        return play_cards

