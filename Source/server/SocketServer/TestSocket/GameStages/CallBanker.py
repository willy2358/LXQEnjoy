from GameStages.GameStage import GameStage

from threading import Timer


class CallBanker(GameStage):
    COMMAND_CALL_BANKER = "call-banker"

    def __init__(self, rule):
        super(CallBanker, self).__init__(rule)
        self.__cur_call_player_idx = -1
        self.__cur_call_action_id = ""
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
            dealer = self.get_round_dealer()
            if dealer:
                for act in call_acts_group.get_actions():
                    act.set_execute_context(player, play_round)
                dealer.send_player_action_group(player, call_acts_group, players)
        else:
            self.__reached_ending_action = True
            if play_round:
                play_round.test_and_update_current_stage()

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
        head_group = self.get_head_action_group()
        if not action_id:
            return head_group
        else:
            act = head_group.get_action_by_id(action_id)
            return act.get_follow_up_action_group()

    def get_notify_players(self):
        return self.get_my_players()

    def process_player_selected_action_id(self, action_id):
        if self.get_head_action_group():
            self.__cur_selected_action = self.get_head_action_group().get_action_by_id(action_id)
            if self.__cur_selected_action :
                self.__cur_selected_action.execute()
