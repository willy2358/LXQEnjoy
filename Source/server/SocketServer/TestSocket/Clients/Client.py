from Rooms.Closet import Closet

class Client:
    def __init__(self, name, clientid, token):
        self.__name = name
        self.__clientid = clientid
        self.__token = token
        self.__products = []
        self.__closets = {}  #{gameid:[]}

    def get_clientid(self):
        return self.__clientid

    def get_available_closet(self, gameid):
        if gameid not in self.__closets:
            self.__closets[gameid] = []

        for c in self.__closets[gameid]:
            if c.is_accept_new_player():
                return c

        rule = self.get_rule_by_gameid(gameid)
        self.__closets[gameid].append(Closet(rule, gameid))

    def get_rule_by_gameid(self, gameid):
        for p in self.__products:
            if p.get_gameid() == gameid:
                return p.get_rule()

        return None



