class PlayerClient:
    def __init__(self, conn):
        self.__socket__conn = conn
        self.__playing_rule_id = 0
        self.__wait_play_ruleid = 0
        self.__play_partners = []

    def set_wait_play_rule_id(self, rule_id):
        self.__playing_rule_id = rule_id

    def set_playing_rule_id(self, rule_id):
        self.__playing_rule_id = rule_id

    def add_play_partner(self, partner):
        if partner != self:
            self.__play_partners.append(partner)

    def get_play_partners(self):
        return self.__play_partners

    def get_socket_conn(self):
        return self.__socket__conn

    def set_player_partners(self, partners):
        for p in partners:
            self.add_play_partner(p)

