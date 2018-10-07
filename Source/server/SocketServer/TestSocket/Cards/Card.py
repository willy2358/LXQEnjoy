
from Cards.GType import GType

class Card:
    CTYPE = "ctype"
    CFIGURE = "cfigure"

    def __init__(self, gtype, ctype, cfigure):
        self.__ctype = ctype
        self.__cfigure = cfigure
        self.__gType = gtype

    @staticmethod
    def create_cards(gtype, ctype, cfigure):
        strType = str(ctype)
        strFig = str(cfigure)

        if strType.startswith("-") or strFig.startswith("-"):
            return []
        if strType.startswith("*") and strFig.startswith("*"):
            return []

        cards = []
        if strType.startswith("*"):
            for t in Card.get_card_ctypes(gtype):
                cards.append(t + strFig)
        if strFig.startswith("*"):
            for f in Card.get_card_figures(gtype, ctype):
                cards.append(strType + f)

        return cards

    @staticmethod
    def get_card_ctypes(gtype):
        if gtype == GType.Poker:
            return ["c", "h", "d", "s", "j"] # club, heart, diamond, spade, joker
        if gtype == GType.Mahong:
            return ["w", "s","t", "f", "z", "h"] #wan, suo, tiao, feng, zhong, hua

    @staticmethod
    def get_card_figures(gtype, ctype):
        if gtype == GType.Poker:
            if ctype == "c" or ctype == "h" or ctype == "d" or ctype == "s":
                return [1,2,3,4,5,6,7,8,9,10,11,12,13] #A,2,3,4,---J,Q,K
            elif ctype == "j":
                return [21, 22]              #moon, sun
            else:
                return []
        if gtype == GType.Mahong:
            if ctype == "w" or ctype == "s" or ctype == "t":
                return [1, 2, 3, 4, 5, 6, 7, 8, 9]
            elif ctype == "f":
                return [1, 3, 5, 7] #dong, nan, xi, bei
            elif ctype == "z":
                return [1, 3, 5]    #zhong, fa, bai
            elif ctype == "h":
                return [1,2,3,4,5,6,7,8] #chun, xia, qiu, dong, mei, lan, zu, ju



