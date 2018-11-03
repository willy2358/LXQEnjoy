
from Mains.GVar import GVar

from Mains.ExtAttrs import ExtAttrs

class Round(ExtAttrs):
    def __init__(self):
        super(Round, self).__init__()
        self.__player_wins = {}