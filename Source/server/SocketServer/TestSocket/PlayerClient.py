import json

import PlayManager


class PlayerClient:
    def __init__(self, conn):
        self.__socket__conn = conn
        self.__playing_rule_id = 0
        self.__wait_play_rule_id = 0
        self.__cards_arranged = False
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

    def send_command_message(self, msg):
        self.__socket__conn.sendall(msg.encode(encoding="utf-8"))

    def begin_new_deal(self):
        self.send_command_message(PlayManager.SERVER_CMD_DEAL_BEGIN)

    def finish_new_deal(self):
        self.send_command_message(PlayManager.SERVER_CMD_DEAL_FINISH)

    def set_cards_arranged(self):
        self.__cards_arranged = True

    def is_cards_arranged(self):
        return self.__cards_arranged

    def deal_one_card(self, card):
        deal = {"card" : card}
        j_str = json.dumps(deal)
        cmdPack = PlayManager.create_command_packet(PlayManager.SERVER_CMD_DEAL_CARD, j_str)
        self.send_command_message(cmdPack)
