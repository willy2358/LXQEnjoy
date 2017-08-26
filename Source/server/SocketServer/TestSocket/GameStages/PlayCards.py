from threading import Timer

from GameStages.GameStage import GameStage


class PlayCards(GameStage):

    COMMAND_PLAY_CARD_CMDS = "play-card-commands"

    def __init__(self, rule):
        super(PlayCards, self).__init__(rule)
        self.__player_idx_of_play_card = -1
        self.__ordered_players = None
        self.__timer_for_default_cards = None
        self.__timer_for_default_cmd = None
        self.__timeout_seconds = 10
        self.__cur_player = None
        self.__reached_round_end = False

    def is_completed(self):
        return self.__reached_round_end

    def begin(self):
        rule = self.get_my_rule()
        my_round = self.get_my_round()
        self.__ordered_players = rule.order_play_card_players(my_round)
        self.let_player_execute_play_cards()

    def let_player_execute_play_cards(self):
        self.reset_action_group()
        rule = self.get_my_rule()
        if rule.get_is_round_end(self.get_my_round()):
            self.__reached_round_end = True
            self.get_my_round().test_and_update_current_stage()
        else:
            player = self.get_next_player()
            act_group = rule.get_play_cards_commands_for_player(player, self.get_my_round())
            act_group.set_select_timeout(2)
            dealer = self.get_round_judger()
            if dealer and act_group:
                self.set_action_group(act_group)
                self.__cur_player = player
                dealer.send_player_action_group(player, act_group, self.get_notify_players())

    def continue_execute(self):
        self.let_player_execute_play_cards()

    def get_notify_players(self):
        return self.get_my_players()

    def get_next_player(self):
        self.__player_idx_of_play_card += 1
        if self.__player_idx_of_play_card >= len(self.__ordered_players):
            self.__player_idx_of_play_card = 0
        if self.__player_idx_of_play_card < len(self.__ordered_players):
            return self.__ordered_players[self.__player_idx_of_play_card]
        else:
            return None

    def process_player_selected_action_id(self, action_id):
        act = self.get_action_by_id(action_id)
        if act:
            act.execute()
