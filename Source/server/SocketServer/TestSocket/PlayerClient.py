#coding=utf-8
import json

import PlayManager

import Utils
import Log

import base64
import os

from datetime import datetime,timedelta

class PlayerClient:
    def __init__(self, conn, user_id):
        self.__socket__conn = conn
        self.__playing_rule_id = 0
        self.__game_round = None
        # self.__initial_cards = []
        self.__cards_in_hand = []   # _cards_in_hand == __active_cards + __freezed_cards
        self.__active_cards = []  # These cards are active, that, these cards can be played out
        self.__freezed_card_groups = []   # These cards are freezed, that is, these cards can not be played out, or used by other purpose
        self.__user_id = user_id
        self.__room_id = 0
        self.__my_room = None
        self.__is_banker = False
        self.__final_cards = None
        self.__final_cards_from_dealer = False   #True, the cards are from dealer, or from the undealed cards, False, these cards from other players
        self.__won_score = 0  # positive, win, negative, lose
        self.__is_online = True
        self.__is_robot_play = False
        self.__session_token = ""
        self.__last_alive_time = datetime.now()

    def is_banker(self):
        return self.__is_banker

    def get_in_hand_cards(self):
        return self.__cards_in_hand

    def get_active_cards(self):
        return self.__active_cards

    def get_user_id(self):
        return self.__user_id

    def get_won_score(self):
        return self.__won_score

    def get_is_online(self):
        return self.__is_online

    def get_is_robot_play(self):
        return self.__is_robot_play

    def get_session_token(self):
        return self.__session_token

    def get_my_room(self):
        return self.__my_room

    def update_connection(self, conn):
        self.__socket__conn = conn
        self.set_is_online(True)

    def set_playing_rule_id(self, rule_id):
        self.__playing_rule_id = rule_id

    def set_game_round(self, round):
        self.__game_round = round

    def set_is_online(self, online=True):
        self.__is_online = online
        if not online:
            self.set_is_robot_play(True)

    def set_is_robot_play(self, robot_play = False):
        self.__is_robot_play = robot_play

    def set_newest_cards(self, cards, is_from_dealer = True, add_in_hand = True):
        self.__final_cards_from_dealer = is_from_dealer
        self.__final_cards = cards
        if add_in_hand:
            self.__cards_in_hand = self.__cards_in_hand + cards

    def set_session_token(self, token):
        self.__session_token = token

    def set_my_room(self, room):
        self.__my_room = room

    def reset_for_next_round(self):
        self.__cards_in_hand = []
        self.__final_cards = []
        self.__active_cards = []
        self.__freezed_card_groups = []
        self.__final_cards = None
        self.__final_cards_from_dealer = False
        self.__won_score = 0  # positive, win, negative, lose
        self.__is_online = True
        self.__is_robot_play = False

    def get_game_round(self):
        return self.__game_round

    def get_final_cards_is_from_dealer(self):
        return self.__final_cards_from_dealer

    def get_final_cards(self):
        return self.__final_cards

    def get_last_alive_time(self):
        return self.__last_alive_time

    def get_socket_conn(self):
        return self.__socket__conn

    def send_command_message(self, msg):

        try:
            self.__socket__conn.sendall(msg.encode(encoding="utf-8"))
            
        except Exception as ex:
            Log.write_exception(ex)

    def begin_new_deal(self):
        self.send_command_message(PlayManager.SERVER_CMD_DEAL_BEGIN)

    def finish_new_deal(self):
        cmd = {"cmd": PlayManager.SERVER_CMD_DEAL_FINISH,
               "recv-resp" :  "resp-" + PlayManager.SERVER_CMD_DEAL_FINISH}
        j_str = json.dumps(cmd)
        self.send_command_message(j_str)

    def set_bank_cards(self, cards):
        self.add_dealed_cards(cards)

    def update_last_alive(self):
        self.__last_alive_time = datetime.now()

    def send_cards_state(self):
        cards1 = self.__active_cards[:]
        cards1.sort()
        str1 = "active cards:" + str(cards1)
        cards2 = self.__freezed_card_groups[:]
        cards2.sort()
        str2 = ";freezed cards:" + str(cards2)
        self.send_command_message(str1 + str2)

    def move_cards_to_freeze_group(self, cards_in_hand, cards_not_in_hand):
        group = cards_in_hand + cards_not_in_hand
        self.__freezed_card_groups.append(group)
        for c in cards_in_hand:
            self.__active_cards.remove(c)
        self.__cards_in_hand = self.__cards_in_hand + cards_not_in_hand
        # self.__final_cards = cards_not_in_hand

    def set_won_score(self, score):
        self.__won_score = score

    def send_server_command(self, cmd_obj):
        # self.send_cards_state() # for viewing data in test client

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

    # def set_initial_cards(self, cards):
    #     self.__initial_cards = cards[:]
    #     self.__cards_in_hand = self.__initial_cards[:]
    #     self.__active_cards = self.__initial_cards[:]

    def add_dealt_cards(self, cards):
        if isinstance(cards, list):
            self.__cards_in_hand += cards
            self.__active_cards += cards
        elif isinstance(cards, int):
            self.__cards_in_hand.append(cards)
            self.__active_cards.append(cards)

        self.set_newest_cards(cards, True, False)

    def play_out_cards(self, cards):
        try:
            if isinstance(cards, int):
                self.__cards_in_hand.remove(cards)
                self.__active_cards.remove(cards)
            elif isinstance(cards, list):
                Utils.list_remove_parts(self.__cards_in_hand, cards)
                for c in cards:
                    self.__active_cards.remove(c)
                    self.__cards_in_hand.remove(c)
            else:
                pass
        except Exception as ex:
            print(ex)
            self.send_command_message(str(ex))

    def set_banker(self):
        self.__is_banker = True

    def reset_banker(self):
        self.__is_banker = False


