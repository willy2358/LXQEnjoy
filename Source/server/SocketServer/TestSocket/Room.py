

class Room:
    def __init__(self, room_id, game_rule):
        self.__room_id = room_id
        self.__game_rule = game_rule
        self.__seated_players = []
        self.__lookon_players = []
        self.__max_seated_players = 0
        self.__min_seated_players = 0
        self.__max_lookon_players = 0

    def is_player_in(self, player):
        return player in self.__players

    def can_new_player_seated(self):
        return len(self.__seated_players) < self.__max_seated_players

    def can_new_player_lookon(self):
        return len(self.__lookon_players) < self.__max_lookon_players

    def add_seated_player(self, player):
        if self.can_new_player_seated():
            self.__players.append(player)
            return True
        else:
            return False
        
    def add_lookon_player(self, player):
        if self.can_new_player_lookon():
            self.__lookon_players.append(player)
            return True
        else:
            return False

    def set_max_seated_player_num(self, max_number):
        self.__max_seated_players = max_number

    def set_min_seated_player_num(self, min_number):
        self.__min_seated_players = min_number

    def set_max_lookon_player_num(self, max_number):
        self.__max_lookon_players = max_number
