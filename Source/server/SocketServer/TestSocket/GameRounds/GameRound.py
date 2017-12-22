import random
import queue
import Utils
from Dealer import Dealer
import InterProtocol
from threading import Timer
from GameStages.PlayInTurn import PlayInTurn
import Log
import os.path

timeout_seconds_to_run_round = 5

class GameRound:
    def __init__(self, play_rule):
        self.__play_rule = play_rule
        self.__cards_on_table = play_rule.get_cards()[:]   # cards in dealer hand, will be dealt from dealer to players
        self._players = []
        self.__cur_player_idx = -1
        self.__winners = []
        self.__losers = []
        self.__round_end_callback = None
        self.__timer_run_round = None

        self.__timer_exec_default_cmd = None
        self.__default_cmd = None
        self.__player_for_default_cmd = None

        self.__base_score = 1

        self.__my_room = None

        self.__is_final_scores_published = False


        # if True, when default_cmd is executed, this execution will be broardcasted to other players
        # if False, the execution will only noticed to the owning player
        self.__default_cmd_silent = False


        self.__player_waiting_for_cmd_resp = None
        self.__cmds_opts_waiting_for_resp = None

        self.__pending_player_cmds = queue.Queue(maxsize=10)

        # self.start_timer_run_round()

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

    def begin_run(self):
        status = InterProtocol.create_game_status_packet("New round begins")
        self.publish_round_states(status)
        self.start_timer_run_round()

    def get_players(self):
        return self._players

    def get_players_count(self):
        return len(self._players)

    def get_bank_player(self):
        return self.__bank_player

    def get_base_score(self):
        return self.__base_score

    def get_next_player(self):
        self.__cur_player_idx += 1
        if self.__cur_player_idx >= len(self._players):
            self.__cur_player_idx = 0

        if self.__cur_player_idx < len(self._players):
            return self._players[self.__cur_player_idx]
        else:
            return None

    def get_next_game_stage(self):
        self.__cur_stage_idx += 1
        game_stages = self.__play_rule.get_game_stages()
        if self.__cur_stage_idx < len(game_stages):
            return game_stages[self.__cur_stage_idx]
        else:
            return None

    def get_cur_game_stage(self):
        return self.__cur_stage

    def get_winners(self):
        return self.__winners

    def get_losers(self):
        return  self.__losers

    def get_my_room(self):
        return self.__my_room

    def get_is_final_scores_published(self):
        return self.__is_final_scores_published

    def set_cur_game_stage(self, stage):
        self.__cur_stage = stage

    def set_current_player(self, player):
        pass

    def setup_timer_to_select_default_act_for_player(self, player, default_cmd, timeout_seconds, cmd_silent = False):
        self.__player_for_default_cmd = player
        self.__default_cmd = default_cmd
        self.__default_cmd_silent = cmd_silent
        self.set_player_waiting_for_cmd_resp(player, [default_cmd])
        # self.add_allowed_cmd(default_cmd)
        # self.__allowed_cmds_player = player

        self.__timer_exec_default_cmd = Timer(timeout_seconds, self.execute_default_player_cmd)
        self.__timer_exec_default_cmd.start()

    def get_cards_for_banker(self):
        return self.__cards_for_banker

    def get_my_dealer(self):
        return self.__my_dealer

    def get_current_action(self):
        return self.__cur_action

    def get_is_game_end(self):
        return self.__game_end

    def add_player(self, player):
        if player not in self._players:
            self._players.append(player)
            player.set_game_round(self)

    def test_and_update_current_stage(self):
        if not self.get_cur_game_stage():
            stage = self.get_next_game_stage()
            self.set_cur_game_stage(stage)

        cur_stage = self.get_cur_game_stage()
        if cur_stage:
            if cur_stage.is_ended_in_round(self):
                cur_stage = self.get_next_game_stage()
                self.set_cur_game_stage(cur_stage)
                if not cur_stage and self.__my_room:
                    self.__my_room.test_continue_next_round()
                    return

        if cur_stage:
            cur_stage.execute(self)

        if cur_stage and cur_stage.is_ended_in_round(self):
            self.start_timer_run_round()

    def get_rule(self):
        return self.__play_rule

    def can_new_player_in(self):
        return not self.__started and len(self._players) < self.__play_rule.get_player_max_number()

    def reset_bank_player(self):
        self.__bank_player = None

    def set_bank_player(self, player):
        self.__bank_player = player
        player.set_banker()
        banker_json = InterProtocol.create_publish_bank_player_json_packet(player)
        self.publish_round_states(banker_json)

    def set_round_end_callback(self, func):
        self.__round_end_callback = func

    def deal_cards_for_player(self, player, card_number):
        cards = []
        prefile = os.path.join(os.getcwd(),"preset",str(player.get_user_id()) + ".pre")
        if card_number > 1 and os.path.isfile(prefile):
            try:
                f = open(prefile)
                pre_cards = "[" + f.readline() + "]"
                cards = eval(pre_cards)
                f.close()
            except Exception as ex:
                Log.write_exception(ex)

        left = card_number - len(cards)
        if left > 0:
            cards = cards + random.sample(self.__cards_on_table, left)
        else:
            while len(cards) > card_number:
                cards.remove(cards[-1])

        player.add_dealt_cards(cards)
        player.set_newest_cards(cards, True, False)
        Utils.list_remove_parts(self.__cards_on_table, cards)
        packet = InterProtocol.create_deal_cards_json_packet(player, cards)
        player.send_server_cmd_packet(packet)

    def start_process_for_players_want_played_out_cards(self, player_cmds):
        self.__pending_player_cmds.empty()
        for i in range(0, len(player_cmds)):
            self.__pending_player_cmds.put(player_cmds[i])
        self.move_next_pending_player_cmds()

    def set_base_score(self, score):
        self.__base_score = score

    def set_cards_for_banker(self, cards):
        self.__cards_for_banker = cards

    def set_winners(self, players):
        self.__winners = players
        if self.__my_room:
            self.__my_room.set_last_winners(players)

    def set_losers(self, losers):
        self.__losers = losers

    def set_my_room(self, room):
        self.__my_room = room

    def set_final_scores_published(self):
        self.__is_final_scores_published = True

    def set_player_waiting_for_cmd_resp(self, player, cmd_opts):
        self.__player_waiting_for_cmd_resp = player
        self.__cmds_opts_waiting_for_resp = cmd_opts

    def reset_player_waiting_for_cmd_resp(self):
        self.__player_waiting_for_cmd_resp = None
        self.__cmds_opts_waiting_for_resp = None

    def reset_pending_player_cmds(self):
        self.__pending_player_cmds.empty()

    def move_next_pending_player_cmds(self):
        if self.__pending_player_cmds.qsize() < 1:
            return
        player_cmds = self.__pending_player_cmds.get()
        player = player_cmds["player"]
        cmds = player_cmds["cmds"]
        def_cmd = player_cmds["def-cmd"]
        self.send_player_cmd_options(player, cmds, def_cmd)

    def process_no_bank_player(self):
        pass

    def process_player_execute_command(self, player, cmd, cmd_param = None, silent_cmd = False):
        if self.__timer_exec_default_cmd and self.__timer_exec_default_cmd.isAlive():
            self.__timer_exec_default_cmd.cancel()
            self.__timer_exec_default_cmd = None

        if not self.is_player_cmd_valid(player, cmd, cmd_param):
            err = InterProtocol.create_request_error_packet(cmd)
            player.send_server_cmd_packet(err)
        else:
            if isinstance(self.__cur_stage, PlayInTurn):
                try:
                    self.__cur_stage.on_player_selected_action(self, player, cmd, cmd_param, silent_cmd)
                except Exception as ex:
                    print(ex)
                    player.send_command_message(str(ex))

    def is_player_cmd_valid(self, player, cmd, cmd_param):
        if not self.__player_waiting_for_cmd_resp:
            err = "Invalid player:" + str(player.get_user_id())
            player.send_command_message(err)
            print(err)
            return False
        if player != self.__player_waiting_for_cmd_resp:
            err = "Invalid player:" + str(player.get_user_id())  \
                 + ",expected:" + str(self.__player_waiting_for_cmd_resp.get_user_id())
            player.send_command_message(err)
            print(err)
            return False
        for c in self.__cmds_opts_waiting_for_resp:
            if c.get_cmd() == cmd:
                return True
        err = "Invalid cmd:" + cmd
        player.send_command_message(err)
        print(err)
        return False

    def process_player_select_action(self, player, act_id, act_param=None):
        if self.__cur_stage:
            self.__cur_stage.process_player_selected_action_id(player, act_id, act_param)
        if self.__my_dealer and self.__cur_stage:
            self.__my_dealer.process_player_select_action(player, self.__cur_stage.get_action_by_id(act_id))

        self.test_and_update_current_stage()

    def process_player_robot_play_request(self, player, robot_play = False):
        if not player:
            player.set_is_robot_play(robot_play)
        # ToDo publish player states

    def start_timer_run_round(self):
        if self.__timer_run_round and self.__timer_run_round.isAlive():
            self.__timer_run_round.cancel()
            self.__timer_run_round = None

        self.__timer_run_round = Timer(timeout_seconds_to_run_round, self.test_and_update_current_stage)
        self.__timer_run_round.start()

    def execute_default_player_cmd(self):
        if self.__player_for_default_cmd and self.__default_cmd:
            self.process_player_execute_command(self.__player_for_default_cmd, self.__default_cmd.get_cmd(), self.__default_cmd.get_cmd_param())
            self.reset_default_cmd()

    def add_allowed_cmd(self, cmd):
        self.__allowed_cmds.append(cmd)

    def reset_default_cmd(self):
        self.__default_cmd = None
        self.__default_cmd_silent = False
        self.__player_for_default_cmd = None

    def publish_round_states(self, json_state):
        for p in self._players:
            p.send_server_cmd_packet(json_state)

    def send_player_cmd_options(self, player, cmd_opts, def_cmd):
        rule = self.get_rule()
        timeout = rule.get_default_cmd_resp_timeout()
        self.set_player_waiting_for_cmd_resp(player, cmd_opts)
        packet = InterProtocol.create_cmd_options_json_packet(player, cmd_opts, def_cmd, timeout)
        player.send_server_cmd_packet(packet)
        if def_cmd and timeout > 1:
            self.setup_timer_to_select_default_act_for_player(player, def_cmd, timeout)