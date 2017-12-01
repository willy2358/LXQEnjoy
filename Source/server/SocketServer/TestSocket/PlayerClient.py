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
        # self.__initial_cards = []
        self.__cards_in_hand = []   # _cards_in_hand == __active_cards + __freezed_cards
        self.__active_cards = []  # These cards are active, that, these cards can be played out
        self.__freezed_card_groups = []   # These cards are freezed, that is, these cards can not be played out, or used by other purpose
        self.__user_id = user_id
        self.__room_id = 0
        self.__is_banker = False
        self.__final_cards = None
        self.__final_cards_from_dealer = False   #True, the cards are from dealer, or from the undealed cards, False, these cards from other players
        self.__won_score = 0  # positive, win, negative, lose

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

    # def get_default_play_cards(self):
    #     if len(self.__initial_cards) > 0:
    #         c = self.__initial_cards[0]
    #         self.__initial_cards.remove(c)
    #         return c
    #     else:
    #         return None

    # def get_init_cards(self):
    #     return self.__initial_cards

    def update_connection(self, conn):
        self.__socket__conn = conn

    def set_playing_rule_id(self, rule_id):
        self.__playing_rule_id = rule_id

    def set_game_round(self, round):
        self.__game_round = round

    def get_game_round(self):
        return self.__game_round

    def get_final_cards_is_from_dealer(self):
        return self.__final_cards_from_dealer

    def get_final_cards(self):
        return self.__final_cards

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
        self.__final_cards = cards_not_in_hand

    def set_final_cards_from_dealer(self, from_dealer = True):
        self.__final_cards_from_dealer = from_dealer

    def set_won_score(self, score):
        self.__won_score = score

    def send_server_command(self, cmd_obj):
        self.send_cards_state() # for viewing data in test client

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
        self.__final_cards = cards
        self.set_final_cards_from_dealer(True)

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


