import random

import Utils
from GameStages import PlayCards
from Dealer import Dealer


class GameRound:
    def __init__(self, play_rule):
        self.__play_rule = play_rule
        self.__players = []
        self.__started = False
        self.__cur_call_player_idx = -1
        self.__cur_call_action_id = ""
        self.__cur_stage = play_rule.get_next_game_stage()
        self.__bank_player = None
        self.__cards_for_banker = None
        self.__player_idx_of_play_card = -1
        self.__my_dealer = Dealer(self)
        self.__cur_action = None
        for s in self.__play_rule.get_game_stages():
            s.set_my_round(self)

    def get_players(self):
        return self.__players

    def get_players_count(self):
        return len(self.__players)

    def get_bank_player(self):
        return self.__bank_player

    def get_cards_for_banker(self):
        return self.__cards_for_banker

    def get_my_dealer(self):
        return self.__my_dealer

    def get_current_action(self):
        return self.__cur_action

    def add_player(self, player):
        self.__players.append(player)
        player.set_game_round(self)

    def test_and_update_current_stage(self):
        if self.__cur_stage:
            if self.__cur_stage.is_completed():
                self.__cur_stage = self.__play_rule.get_next_game_stage()
                self.__cur_stage.begin()
            else:
                self.__cur_stage.continue_execute()

    def get_rule(self):
        return self.__play_rule

    def can_new_player_in(self):
        return not self.__started and len(self.__players) < self.__play_rule.get_player_max_number()

    def set_bank_player(self, player):
        self.__bank_player = player

    def execute_player_call(self, player, call):
        action = self.__play_rule.get_action_by_id(call["act-id"])
        self.__cur_stage.publish_player_call_action(player, action)

    def execute_player_played_cards(self, player, cards):
        if isinstance(self.__cur_stage, type(PlayCards)):
            self.__cur_stage.publish_player_play_cards(player, cards["cards"])
        else:
            pass

    def set_cards_for_banker(self, cards):
        self.__cards_for_banker = cards

    def process_no_bank_player(self):
        pass

    def process_player_select_action(self, player, act_id):
        if self.__cur_stage:
            self.__cur_stage.process_player_selected_action_id(act_id)
        if self.__my_dealer and self.__cur_stage:
            self.__my_dealer.process_player_select_action(player, self.__cur_stage.get_action_by_id(act_id))

        self.test_and_update_current_stage()