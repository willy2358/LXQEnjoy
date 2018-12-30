from enum import Enum
from Cards.GType import GType

TOKEN = "ctype"

def parse_ctype(strCtype, gType = GType.Poker):
    if gType == GType.Poker:
        if strCtype.startswith('c'):
            return CType.P_Club
        elif strCtype.startswith('d'):
            return CType.P_Diamond
        elif strCtype.startswith('h'):
            return CType.P_Heart
        elif strCtype.startswith('j'):
            return CType.P_Joker
        elif strCtype.startswith('s'):
            return CType.P_Spade
        elif strCtype.startswith('*'):
            return CType.Any
        elif strCtype.startswith('-'):
            return CType.Undefined
    elif gType == GType.Mahong:
        if strCtype.startswith('w'):
            return CType.M_Wan
        elif strCtype.startswith('s'):
            return CType.M_Suo
        elif strCtype.startswith('t'):
            return CType.M_Tong
        elif strCtype.startswith('f'):
            return CType.M_Feng
        elif strCtype.startswith('a'):
            return CType.M_Arrow
    else:
        return CType.Undefined



class CType(Enum):
    Any = "*"
    Undefined = "-"
    P_Club = "c"
    P_Diamond = "d"
    P_Heart = "h"
    P_Spade = "s"
    P_Joker = "j"

    M_Wan = "w"
    M_Suo = "s"
    M_Tong = "t"
    M_Feng = "f"
    M_Arrow = "a"

    @staticmethod
    def get_type_str(cType):
        if cType == CType.P_Club:
            return 'c'
        elif cType == CType.P_Diamond:
            return 'd'
        elif cType == CType.P_Heart:
            return 'h'
        elif cType == CType.P_Spade:
            return 's'
        elif cType == CType.P_Joker:
            return 'j'
        elif cType == cType.M_Wan:
            return 'w'
        elif cType == CType.M_Suo:
            return 's'
        elif cType == CType.M_Tong:
            return 't'
        elif cType == CType.M_Feng:
            return 'f'
        elif cType == CType.M_Arrow:
            return 'a'
        else:
            return 'undef'

