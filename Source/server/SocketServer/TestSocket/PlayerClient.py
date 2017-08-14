#coding=utf-8
import json

import PlayManager

from threading import Timer


class PlayerClient:
    def __init__(self, conn):
        self.__socket__conn = conn
        self.__playing_rule_id = 0
        self.__wait_play_rule_id = 0
        self.__cards_arranged = False
        self.__play_partners = []
        self.__game_round = None
        self.__pre_call_action = None
        self.__my_call_action = None
        self.__timer_for_call = None
        self.__recv_resps = []

    def set_wait_play_rule_id(self, rule_id):
        self.__playing_rule_id = rule_id

    def set_playing_rule_id(self, rule_id):
        self.__playing_rule_id = rule_id

    def add_play_partner(self, partner):
        if partner != self:
            self.__play_partners.append(partner)

    def add_recv_resp(self, resp):
        self.__recv_resps.append(resp)

    def set_game_round(self, round):
        self.__game_round = round

    def get_game_round(self):
        return self.__game_round

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
        cmd = {"cmd": PlayManager.SERVER_CMD_DEAL_FINISH,
               "recv-resp" :  "resp-" + PlayManager.SERVER_CMD_DEAL_FINISH}
        j_str = json.dumps(cmd)
        self.send_command_message(j_str)

    def send_call_command_options(self, act_group):
        # cmd = '{"actions":['
        # for c in act_group.get_actions():
        #     cmd += c.to_json() + ","
        #     if c.get_is_default():
        #         self.__pre_call_action = c
        # cmd += "]}"
        self.__pre_call_action = act_group.get_default_action()
        cmd = act_group.to_json()
        self.start_timer_to_tell_server_my_action(act_group.get_select_timeout())

        cmd_pack = PlayManager.create_command_packet(PlayManager.SERVER_CMD_CALL_ACTIONS, cmd)
        self.send_command_message(cmd_pack)

    def set_cards_sorted(self):
        self.__cards_arranged = True

    def reset_call_actions(self):
        self.__my_call_action = None
        self.__pre_call_action = None

    def is_cards_sorted(self):
        return self.__cards_arranged

    def process_cards_sorted(self):
        self.set_cards_sorted()
        self.__game_round.process_player_cards_sorted()

    def deal_one_card(self, card):
        deal = {"card": card}
        j_str = json.dumps(deal)
        cmd_pack = PlayManager.create_command_packet(PlayManager.SERVER_CMD_DEAL_CARD, j_str)
        self.send_command_message(cmd_pack)
    
    def start_timer_to_tell_server_my_action(self, timeout_seconds):
        self.__timer_for_call = Timer(timeout_seconds, self.apply_default_action_as_my_action)
        self.__timer_for_call.start()

    def apply_default_action_as_my_action(self):
        if self.__pre_call_action:
            self.tell_server_my_action(self.__pre_call_action)

    def tell_server_my_action(self, action):
        self.__game_round.make_next_player_select_action(action.get_action_id())

    def update_my_call_action(self, action_id):
        if self.__pre_call_action:
            self.__pre_call_action = None

        if self.__timer_for_call:
            self.__timer_for_call.cancel()
            self.__timer_for_call = None
        self.get_game_round().make_next_player_select_action(action_id)

"""
join_game#{"rule_id":"1212"}
{"req":"join-game", "rule_id":"1212"}
 
cards_sorted
select_call#{"action_id":"1"}
"""

