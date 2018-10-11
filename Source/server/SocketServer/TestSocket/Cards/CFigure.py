from enum import Enum

TOKEN = "cfigure"

def parse_cfigure(strFig):
    if strFig.startswith('*'):
        return CFigure.Any
    elif strFig.startswith('-'):
        return CFigure.Undefined
    elif strFig.isnumeric():
        return CFigure(int(strFig))
    else:
        return CFigure.Undefined

class CFigure(Enum):
    Any = 100
    Undefined = -1
    Fig_1 = 1
    Fig_2 = 2
    Fig_3 = 3
    Fig_4 = 4
    Fig_5 = 5
    Fig_6 = 6
    Fig_7 = 7
    Fig_8 = 8
    Fig_9 = 9

    Fig_10 = 10
    Fig_11 = 11
    Fig_12 = 12
    Fig_13 = 13
    Fig_14 = 14
    Fig_15 = 15
    Fig_16 = 16
    Fig_17 = 17
    Fig_18 = 18
    Fig_19 = 19

    Fig_20 = 20
    Fig_21 = 21
    Fig_22 = 22
    Fig_23 = 23
    Fig_24 = 24
    Fig_25 = 25
    Fig_26 = 26
    Fig_27 = 27
    Fig_28 = 28
    Fig_29 = 29

    Fig_30 = 30
    Fig_31 = 31
    Fig_32 = 32
    Fig_33 = 33
    Fig_34 = 34
    Fig_35 = 35
    Fig_36 = 36
    Fig_37 = 37
    Fig_38 = 38
    Fig_39 = 39

