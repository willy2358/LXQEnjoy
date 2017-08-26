#coding=utf-8
import json

import PlayManager

from threading import Timer

import Utils


class PlayerClient:
    def __init__(self, conn):
        self.__socket__conn = conn
        self.__playing_rule_id = 0
        self.__game_round = None
        self.__dealed_cards = []
        self.__remained_cards = []

    def get_remained_cards(self):
        return self.__remained_cards

    def get_default_play_cards(self):
        if len(self.__dealed_cards) > 0:
            c = self.__dealed_cards[0]
            self.__dealed_cards.remove(c)
            return c
        else:
            return None

    def set_playing_rule_id(self, rule_id):
        self.__playing_rule_id = rule_id

    def set_game_round(self, round):
        self.__game_round = round

    def get_game_round(self):
        return self.__game_round

    def get_socket_conn(self):
        return self.__socket__conn

    def send_command_message(self, msg):
        self.__socket__conn.sendall(msg.encode(encoding="utf-8"))

    def begin_new_deal(self):
        self.send_command_message(PlayManager.SERVER_CMD_DEAL_BEGIN)

    def finish_new_deal(self):
        cmd = {"cmd": PlayManager.SERVER_CMD_DEAL_FINISH,
               "recv-resp" :  "resp-" + PlayManager.SERVER_CMD_DEAL_FINISH}
        j_str = json.dumps(cmd)
        self.send_command_message(j_str)

    def set_bank_cards(self, cards):
        self.add_dealed_cards(cards)

    def send_server_command(self, cmd_obj):
        j_str = json.dumps(cmd_obj)
        self.send_command_message(j_str)

    def add_dealed_cards(self, cards):
        if isinstance(cards, list):
            self.__dealed_cards += cards
        elif isinstance(cards, str):
            self.__dealed_cards.append(cards)

        self.__remained_cards = self.__dealed_cards[:]

    def play_out_cards(self, cards):
        if isinstance(cards, str):
            self.__remained_cards.remove(cards)
        elif isinstance(cards, list):
            Utils.list_remove_parts(self.__remained_cards, cards)
        else:
            pass



