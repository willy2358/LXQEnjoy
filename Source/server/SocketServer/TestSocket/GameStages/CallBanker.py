from GameStages.GameStage import GameStage


class CallBanker(GameStage):
    COMMAND_CALL_BANKER = "call-banker"
    def __init__(self, rule):
        super(CallBanker, self).__init__(rule)
        self.__cur_call_player_idx = -1
        self.__cur_call_action_id = ""

    def is_completed(self):
        return False

    def begin(self):
        self.begin_players_call_process()

    def begin_players_call_process(self):
        self.make_next_player_select_action(None)

    def make_next_player_select_action(self, prev_action_id):
        player = self.get_next_call_player()
        call_acts_group = self.get_next_call_action_group(prev_action_id)
        if player and call_acts_group:
            cmd_obj = {"cmd": CallBanker.COMMAND_CALL_BANKER,
                       "actions": call_acts_group.to_json() }
            # player.send_call_command_options(call_acts_group)
            player.send_server_command(cmd_obj)

    def get_next_call_player(self):
        self.__cur_call_player_idx += 1
        players = self.get_my_players()
        if self.__cur_call_player_idx >= len(players):
            self.__cur_call_player_idx = 0
        if self.__cur_call_player_idx < len(players):
            return players[self.__cur_call_player_idx]
        else:
            return None

    def get_next_call_action_group(self, action_id):
        return self.get_my_rule().get_follow_up_action_group(action_id)