from threading import Timer

import PlayRound


class Judger:
    COMMAND_OPTIONS = "cmd-opts"
    CLIENT_RESP_SELECT_ACTION = "select-act"

    def __init__(self, play_round):
        assert isinstance(play_round, PlayRound)
        self.__my_play_round = play_round
        self.__timer_wait_player = None
        self.__default_player_action = None
        self.__player_accept_command = None
        self.__select_action_publish_players = None
        self.__sent_action_group = None

    def send_player_action_group(self, player, act_group, select_publish_players):
        self.__player_accept_command = player
        self.__select_action_publish_players = select_publish_players
        if player and act_group:
            self.__sent_action_group = act_group
            self.__default_player_action = act_group.get_default_action()
            self.start_timer_to_wait_player_response(act_group.get_select_timeout())
            cmd_obj = {"cmd": Judger.COMMAND_OPTIONS,
                       "opts": act_group.to_json()}
            player.send_server_command(cmd_obj)

    def start_timer_to_wait_player_response(self, timeout_seconds):
        self.__timer_wait_player = Timer(timeout_seconds, self.select_default_action)
        self.__timer_wait_player.start()

    def select_default_action(self):
        self.process_player_select_action(self.__player_accept_command, self.__default_player_action)

    def process_player_select_action_of_id(self, player, action_id):
        action = self.get_action_by_id(action_id)
        if action:
            self.process_player_select_action(player, action)

    def process_player_select_action(self, player, action):
        self.reset_timer()
        if self.__select_action_publish_players:
            resp = {"resp": Judger.CLIENT_RESP_SELECT_ACTION }
            for p in self.__select_action_publish_players:
                p.send_server_command(resp)

    def get_action_by_id(self, action_id):
        if self.__sent_action_group:
            return self.__sent_action_group.get_action_by_id(action_id)
        else:
            return None

    def reset_timer(self):
        if self.__default_player_action:
            self.__default_player_action = None

        if self.__timer_wait_player:
            if self.__timer_wait_player.isAlive():
                self.__timer_wait_player.cancel()
            self.__timer_wait_player = None
