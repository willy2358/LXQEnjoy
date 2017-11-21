import random

import Utils
from GameStages import PlayCards
from Dealer import Dealer
import InterProtocol
from threading import Timer


class GameRound:
    def __init__(self, play_rule):
        self.__play_rule = play_rule
        self.__cards_on_table = play_rule.get_cards()[:]   # cards in dealer hand, will be dealt from dealer to players
        self.__players = []
        self.__cur_player_idx = -1
        self.__winners = []
        self.__losers = []
        self._round_end_callback = None
        self._timer_run_round = None
        self.start_timer_run_round()

        self.__started = False
        self.__cur_call_player_idx = -1
        self.__cur_call_action_id = ""
        self.__cur_stage = None
        self.__cur_stage_idx = -1
        self.__bank_player = None
        self.__cards_for_banker = None
        self.__player_idx_of_play_card = -1
        self.__my_dealer = Dealer(self)
        self.__cur_action = None
        self.__game_end = False

    def get_players(self):
        return self.__players

    def get_players_count(self):
        return len(self.__players)

    def get_bank_player(self):
        return self.__bank_player

    def get_next_player(self):
        self.__cur_player_idx += 1
        if self.__cur_player_idx >= len(self.__players):
            self.__cur_player_idx = 0

        if self.__cur_player_idx < len(self.__players):
            return self.__players[self.__cur_player_idx]
        else:
            return None

    def get_next_game_stage(self):
        self.__cur_player_idx += 1
        game_stages = self.__play_rule.get_game_stages()
        if self.__cur_player_idx < len(game_stages):
            return game_stages[self.__cur_player_idx]
        else:
            return None

    def get_cur_game_stage(self):
        return self.__cur_stage

    def get_winners(self):
        return self.__winners

    def get_losers(self):
        return  self.__losers

    def set_cur_game_stage(self, stage):
        self.__cur_stage = stage

    def set_current_player(self, player):
        pass

    def setup_timer_to_select_default_act_for_player(self, player, default_cmd, cmd_param, timeout_seconds):
        pass

    def get_cards_for_banker(self):
        return self.__cards_for_banker

    def get_my_dealer(self):
        return self.__my_dealer

    def get_current_action(self):
        return self.__cur_action

    def get_is_game_end(self):
        return self.__game_end

    def add_player(self, player):
        if player not in self.__players:
            self.__players.append(player)
            player.set_game_round(self)

    def test_and_update_current_stage(self):
        if not self.get_cur_game_stage():
            stage = self.get_next_game_stage()
            self.set_cur_game_stage(stage)

        cur_stage = self.get_cur_game_stage()
        if cur_stage:
            if cur_stage.is_ended_in_round(self):
                cur_stage = self.get_next_game_stage()
                if not cur_stage and self._round_end_callback:
                    self._round_end_callback()

        if cur_stage:
            cur_stage.execute(self)

        if cur_stage and cur_stage.is_ended_in_round(self):
            self.start_timer_run_round()

    def get_rule(self):
        return self.__play_rule

    def can_new_player_in(self):
        return not self.__started and len(self.__players) < self.__play_rule.get_player_max_number()

    def reset_bank_player(self):
        self.__bank_player = None

    def set_bank_player(self, player):
        self.__bank_player = player
        player.set_banker()
        banker_json = InterProtocol.create_publish_bank_player_json_packet(player)
        self.publish_round_states(banker_json)

    def set_round_end_callback(self, func):
        self._round_end_callback = func

    def deal_cards_for_player(self, player, card_number):
        cards = random.sample(self.__cards_on_table, card_number)
        player.set_initial_cards(cards)
        Utils.list_remove_parts(self.__cards_on_table, cards)
        packet = InterProtocol.create_deal_cards_json_packet(player, cards)
        player.send_server_command(packet)

    def set_cards_for_banker(self, cards):
        self.__cards_for_banker = cards

    def set_winners(self, players):
        self.__winners = players

    def process_no_bank_player(self):
        pass

    def process_player_select_action(self, player, act_id, act_param=None):
        if self.__cur_stage:
            self.__cur_stage.process_player_selected_action_id(player, act_id, act_param)
        if self.__my_dealer and self.__cur_stage:
            self.__my_dealer.process_player_select_action(player, self.__cur_stage.get_action_by_id(act_id))

        self.test_and_update_current_stage()

    def start_timer_run_round(self):
        self._timer_run_round = Timer(10, self.test_and_update_current_stage)
        self._timer_run_round.start()

    def publish_round_states(self, json_state):
        for p in self.__players:
            p.send_server_command(json_state)
