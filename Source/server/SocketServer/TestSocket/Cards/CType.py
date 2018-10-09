from enum import Enum

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
