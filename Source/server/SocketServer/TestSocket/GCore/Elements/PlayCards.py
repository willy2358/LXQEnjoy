
from GCore.Statement import Statement
class PlayCards(Statement):
    def __init__(self, player, cards, act_alias, cards_face_up=True):
        super(PlayCards, self).__init__()
        self.__player = player
        self.__cards = cards
        self.__act_alias = act_alias
        self.__cards_face_up = cards_face_up


    def gen_runtime_obj(self, scene):
        pass

