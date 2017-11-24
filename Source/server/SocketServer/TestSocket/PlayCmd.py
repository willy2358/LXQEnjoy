
class PlayCmd:
    def __init__(self, player, cmd):
        self.__player = player
        self.__cmd = cmd
        self.__cmd_param = []

    def get_cmd(self):
        return self.__cmd

    def get_cmd_param(self):
        return self.__cmd_param

    def get_cmd_player(self):
        return self.__player

    def set_cmd_param(self, cards):
        self.__cmd_param = cards
