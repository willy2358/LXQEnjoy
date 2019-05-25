from Mains import PlayManager

from datetime import datetime
import Utils

import Mains.InterProtocol as InterProtocol

# from Mains.GVar import GVar
from Mains.ExtAttrs import ExtAttrs

class Player(ExtAttrs):
    def __init__(self, userid):
        super(Player, self).__init__()
        self.__userid = userid
        self.__token = None
        self.__sock_conn = None
        self.__room = None
        self.__closet = None
        self.__last_alive_time = datetime.now()
        self.__seatid = 0
        self.__last_sent_cmd_str = ""

        self.__is_online = True
        self.__is_robot_play = False
        # self.__cards_in_hand = []
        self.__free_cards = []
        self.__frozen_cards = []
        self.__shown_cards = [] #[[],[]]


    def get_userid(self):
        return self.__userid

    def get_token(self):
        return self.__token

    def get_sock_conn(self):
        return self.__sock_conn

    def get_room(self):
        return self.__room

    def get_closet(self):
        return self.__closet

    def get_seatid(self):
        return self.__seatid

    def get_is_online(self):
        return self.__is_online

    def get_is_robot_play(self):
        return self.__is_robot_play

    def get_free_cards(self):
        return self.__free_cards[:]

    def has_cards(self, cards):
        #考虑到cards中有多张相同牌的可能
        tmpCards = self.__free_cards[:]
        #ToDo optimization is need, since tmpCards can not be changed in for loop
        for c in tmpCards:
            if c not in tmpCards:
                return False
            else:
                tmpCards.remove(c)
        return True

    def pick_cards(self, count):
        return self.__free_cards[:count]

    def play_cards(self, cards):
        Utils.list_remove_parts(self.__free_cards, cards)

    def set_sock_conn(self, conn):
        self.__sock_conn = conn

    def set_token(self, token):
        self.__token = token

    def set_room(self, room):
        self.__room = room

    def set_closet(self, closet):
        self.__closet = closet

    def set_seatid(self, seatid):
        self.__seatid = seatid

    def set_is_robot_play(self, robot_play = False):
        self.__is_robot_play = robot_play

    def send_cards(self, cards):
        self.__free_cards += cards
        packet = InterProtocol.create_deal_cards_json_packet(self, cards)
        self.send_server_cmd_packet(packet)

    def publish_message(self, msgTxt):
        if msgTxt:
            packet = InterProtocol.create_msg_packet(msgTxt)
            self.send_server_cmd_packet(packet)

    def set_is_online(self, online=True):
        self.__is_online = online
        if not online:
            self.set_is_robot_play(True)

    def update_connection(self, conn):
        self.__sock_conn = conn
        self.set_is_online(True)
        self.update_last_alive()

        cmd_str_bak = self.__last_sent_cmd_str
        pack = InterProtocol.create_cards_state_packet(self)
        self.send_server_cmd_packet(pack)

        if cmd_str_bak:
            self.send_raw_network_data(cmd_str_bak)
    def pub_my_status(self):
        status = self.get_pub_status()
        pack = InterProtocol.create_game_status_packet(InterProtocol.server_push_player_status, status)
        self.send_server_cmd_packet(pack)

    def update_last_alive(self):
        self.__last_alive_time = datetime.now()

    def response_success_pack(self, pack):
        PlayManager.send_pack_to_client(self.__sock_conn, pack)

    def response_err_pack(self, cmd, err_code, errArg=None):
        PlayManager.send_err_pack_to_client(self.__sock_conn, cmd, err_code, errArg)

    def send_server_cmd_packet(self, pack):
        return PlayManager.send_pack_to_client(self.__sock_conn, pack)