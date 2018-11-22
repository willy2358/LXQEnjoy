
class PlayCmd:
    def __init__(self, player, cmd, cmd_param = None):
        self.__player = player
        self.__cmd = cmd
        self.__cmd_param = []
        if isinstance(cmd_param, list):
            self.__cmd_param = cmd_param
        elif cmd_param:
            self.__cmd_param = [cmd_param]

        self.__is_silent = False

    def get_cmd(self):
        return self.__cmd

    def get_cmd_param(self):
        return self.__cmd_param

    def get_cmd_player(self):
        return self.__player

    def set_cmd_player(self, player):
        self.__player = player

    def is_silent(self):
        return self.__is_silent

    def set_cmd_param(self, cards):
        if isinstance(cards, type([])):
            self.__cmd_param = cards
        else:
            self.__cmd_param = [cards]

    def set_silent_flag(self, is_silent):
        self.__is_silent = is_silent
