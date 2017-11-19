#coding=utf-8
import json

import PlayManager

from threading import Timer

import Utils
import Log


class PlayerClient:
    def __init__(self, conn, user_id):
        self.__socket__conn = conn
        self.__playing_rule_id = 0
        self.__game_round = None
        self.__initial_cards = []
        self.__cards_in_hand = []
        self.__user_id = user_id
        self.__room_id = 0
        self.__is_banker = False

    def is_banker(self):
        return self.__is_banker

    def get_in_hand_cards(self):
        return self.__cards_in_hand

    def get_user_id(self):
        return self.__user_id

    def get_default_play_cards(self):
        if len(self.__initial_cards) > 0:
            c = self.__initial_cards[0]
            self.__initial_cards.remove(c)
            return c
        else:
            return None

    def get_init_cards(self):
        return self.__initial_cards

    def update_connection(self, conn):
        self.__socket__conn = conn

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

    def send_error_message(self, req_cmd, errmsg):
        Log.write_error(errmsg)
        msg = {"cmdtype": "sockresp",
               "sockresp":req_cmd,
               "result":"ERROR",
               "errmsg":errmsg}
        j_str = json.dumps(msg)
        self.send_command_message(j_str)

    def send_success_message(self, req_cmd):
        msg = {"cmdtype": "sockresp",
                    "sockresp":req_cmd,
                    "result":"OK",
                    "errmsg":""}
        j_str = json.dumps(msg)
        self.send_command_message(j_str)

    def set_initial_cards(self, cards):
        self.__initial_cards = cards[:]
        self.__cards_in_hand = self.__initial_cards[:]

    def add_dealt_cards(self, cards):
        if isinstance(cards, list):
            self.__initial_cards += cards
        elif isinstance(cards, str):
            self.__initial_cards.append(cards)

        self.__cards_in_hand = self.__initial_cards[:]

    def play_out_cards(self, cards):
        if isinstance(cards, str):
            self.__cards_in_hand.remove(cards)
        elif isinstance(cards, list):
            Utils.list_remove_parts(self.__cards_in_hand, cards)
        else:
            pass

    def set_banker(self):
        self.__is_banker = True

    def reset_banker(self):
        self.__is_banker = False


