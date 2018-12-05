
from GCore.Statement import Statement
import Mains.Log as Log

class PlayCards(Statement):
    def __init__(self, player, cards, act_alias, cards_face_up=True, quiet=False):
        super(PlayCards, self).__init__()
        self.__player = player
        self.__cards = cards
        self.__act_alias = act_alias

        # if true, a * is used to represent a card, that is, the other players do not known the concrete card face
        self.__cards_face_up = cards_face_up

        # if True, do not tell other players
        self.__quiet = quiet


    def gen_runtime_obj(self, scene):
        def play_cards():
            try:
                player = scene.get_obj_value(self.__player)
                cards = scene.get_obj_value(self.__cards)
                if player and cards:
                    face_up = scene.get_obj_value(self.__cards_face_up)
                    quiet = scene.get_obj_value(self.__quiet)
                    scene.process_player_play_cards(player, cards, face_up, quiet)

            except Exception as ex:
                Log.exception(ex)

        return play_cards

