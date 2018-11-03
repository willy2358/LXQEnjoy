
from Cards.GType import GType

_Poker_Cards = ["c1","d1", "h1", "s1",
            "c2", "d2", "h2", "s2",
            "c3", "d3", "h3", "s3",
            "c4", "d4", "h4", "s4",
            "c5", "d5", "h5", "s5",
            "c6", "d6", "h6", "s6",
            "c7", "d7", "h7", "s7",
            "c8", "d8", "h8", "s8",
            "c9", "d9", "h9", "s9",
            "c10", "d10", "h10", "s10",
            "c11", "d11", "h11", "s11",
            "c12", "d12", "h12", "s12",
            "c13", "d13", "h13", "s13",
             "j21", "j22"]

Mahong_ws = ["w1","w2","w3","w4","w5","w6","w7","w8","w9"] * 4
Mahong_ss = ["s1","s2","s3","s4","s5","s6","s7","s8","s9"] * 4
Mahong_ts = ["t1","t2","t3","t4","t5","t6","t7","t8","t9"] * 4
Mahong_fs = ["f1","f3","f5","f7"] * 4
Mahong_zs = ["z1","z3","z5"] * 4
Mahong_hs = ["h1","h2","h3","h4","h5","h6","h7","h8"]

_Mahong_Cards = Mahong_ws + Mahong_ss + Mahong_ts + Mahong_fs + Mahong_zs + Mahong_hs

def get_cards(gType):
    if gType == GType.Poker:
        return _Poker_Cards[:]
    elif gType == GType.Mahong:
        return _Mahong_Cards[:]
    else:
        return None

class Card:
    CTYPE = "ctype"
    CFIGURE = "cfigure"

    def __init__(self, gtype, ctype, cfigure):
        self.__ctype = ctype
        self.__cfigure = cfigure
        self.__gType = gtype
        self.__score = 0;

    def set_score(self, score):
        self.__score = score



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
                cards.append(Card(gtype, t, strFig))
        elif strFig.startswith("*"):
            for f in Card.get_card_figures(gtype, ctype):
                cards.append(Card(gtype, strType, f))
        else:
            cards.append(Card(gtype, ctype, cfigure))

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



