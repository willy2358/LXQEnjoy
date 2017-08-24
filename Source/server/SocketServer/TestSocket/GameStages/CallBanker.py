from GameStages.GameStage import GameStage

from threading import Timer


class CallBanker(GameStage):
    COMMAND_CALL_BANKER = "call-banker"

    def __init__(self, rule):
        super(CallBanker, self).__init__(rule)
        self.__cur_call_player_idx = -1
        self.__cur_call_action_id = ""
        # self.__pre_call_action = None
        # self.__timer_for_call = None
        self.__current_player = None
        self.__reached_ending_action = False
        self.__cur_selected_action = None

    def is_completed(self):
        return self.__reached_ending_action

    def begin(self):
        self.begin_players_call_process()

    def continue_execute(self):
        play_round = self.get_my_round()
        if play_round:
            act = self.__cur_selected_action
            if act:
                self.make_next_player_select_action(act.get_act_id())
            else:
                pass
        else:
            pass

    def begin_players_call_process(self):
        self.make_next_player_select_action(None)

    def make_next_player_select_action(self, prev_action_id):

        call_acts_group = self.get_next_call_action_group(prev_action_id)
        play_round = self.get_my_round()
        if call_acts_group:
            player = self.get_next_call_player()
            players = self.get_notify_players()
            self.__current_player = player
            if play_round:
                judger = play_round.get_judger()
                if judger:
                    judger.send_player_action_group(player, call_acts_group, players)
        else:
            self.__reached_ending_action = True
            if play_round:
                play_round.test_and_update_current_stage()


        # if player and call_acts_group:
        #     self.__pre_call_action = call_acts_group.get_default_action()
        #     self.start_timer_to_publish_player_call_action(call_acts_group.get_select_timeout())
        #     self.tell_player_to_select_call_actions(player, call_acts_group)

    # def tell_player_to_select_call_actions(self, player, act_group):
    #     cmd_obj = {"cmd": CallBanker.COMMAND_CALL_BANKER,
    #                "actions": act_group.to_json()}
    #     self.__current_player = player
    #     player.send_server_command(cmd_obj)
                 
    def get_next_call_player(self):
        self.__cur_call_player_idx += 1
        players = self.get_my_players()
        if self.__cur_call_player_idx >= len(players):
            self.__cur_call_player_idx = 0
        if self.__cur_call_player_idx < len(players):
            return players[self.__cur_call_player_idx]
        else:
            return None

    # def start_timer_to_publish_player_call_action(self, timeout_seconds):
    #     self.__timer_for_call = Timer(timeout_seconds, self.publish_default_action_as_player_call)
    #     self.__timer_for_call.start()

    # def publish_default_action_as_player_call(self):
    #     if self.__pre_call_action:
    #         self.publish_player_call_action(self.__current_player, self.__pre_call_action)

    # def tell_server_my_action(self, action):
    #     self.get_my_round().make_next_player_select_action(action.get_action_id())

    def get_next_call_action_group(self, action_id):
        head_group = self.get_head_action_group()
        if not action_id:
            return head_group
        else:
            act = head_group.get_action_by_id(action_id)
            return act.get_follow_up_action_group()

    # def publish_player_call_action(self, player, action):
    #     self.reset_default_call_timer()
    #
    #     for p in self.get_notify_players():
    #         info = {"info": "player-call"}
    #         p.send_server_command(info)
    #
    #     if action.get_is_bank_action():
    #         self.get_my_round().set_bank_player(player)
    #
    #     call_acts_group = self.get_next_call_action_group(action.get_action_id())
    #     if not call_acts_group:
    #         self.__reached_ending_action = True
    #         self.get_my_round().test_and_update_current_stage()
    #         return
    #
    #     self.make_next_player_select_action(action.get_action_id())
        # next_player = self.get_next_call_player()
        # call_group = self.get_next_call_action_group(action.get_action_id())
        # if next_player and call_group:
        #     self.tell_player_to_select_call_actions(next_player, call_group)

    def get_notify_players(self):
        return self.get_my_players()

    # def reset_default_call_timer(self):
    #     if self.__pre_call_action:
    #         self.__pre_call_action = None
    #     if self.__timer_for_call:
    #         if self.__timer_for_call.isAlive():
    #             self.__timer_for_call.cancel()
    #         self.__timer_for_call = None

    def process_player_selected_action_id(self, action_id):
        if self.get_head_action_group():
            self.__cur_selected_action = self.get_head_action_group().get_action_by_id(action_id)
            if self.__cur_selected_action and self.__cur_selected_action.get_is_call_banker():
                self.get_my_round().set_bank_player(self.__current_player)
