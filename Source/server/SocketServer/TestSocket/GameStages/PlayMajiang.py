from GameStages.PlayInTurn import PlayInTurn
from PlayCmd import PlayCmd
import InterProtocol


# terms: one-play: includes:
# letting one player play one card, this play is called the starter
# this player played one card
# letting other players response to the played card, these players are called listeners
# one listener got the played card or got a new card from table
# this listener become the starter of new one-play, new one-play begins
class PlayMajiang(PlayInTurn):
    def __init__(self, rule):
        pass

    @staticmethod
    def execute(game_round):
        rule = game_round.get_rule()
        starter = game_round.get_bank_player()
        cmd_opts = rule.get_player_cmd_options_for_cards(starter, [], True, False)
        if not cmd_opts:
            cmd_opts.append(PlayCmd(starter, InterProtocol.majiang_player_act_play_card))

        PlayMajiang.send_player_cmd_options(game_round, starter, cmd_opts, cmd_opts[0])

    @staticmethod
    def is_ended_in_round(game_round):
        winners = game_round.get_winners()
        if len(winners) > 0:
            return True
        else:
            return False

    @staticmethod
    def send_player_cmd_options(game_round, player, cmd_opts, def_cmd):
        rule = game_round.get_rule()
        timeout = rule.get_default_cmd_resp_timeout()
        # cmd_opts = rule.get_player_cmd_options_for_cards(starter, new_cards, is_turn_ordered, is_played_out_cards)
        packet = InterProtocol.create_cmd_options_json_packet(player, cmd_opts, def_cmd, timeout)
        player.send_server_command(packet)
        if def_cmd and timeout > 1:
            game_round.setup_timer_to_select_default_act_for_player(player, def_cmd, timeout)

    @staticmethod
    def on_one_card_played_out(game_round, player, played_card):
        listeners = game_round.get_one_play_listeners(player)
        rule = game_round.get_rule()
        players_cmd_opts = []
        for p in listeners:
            cmd_opts = rule.get_player_cmd_options_for_cards(p, [played_card], p == listeners[0], True)
            players_cmd_opts.append({
                "player":p,
                "cmds":cmd_opts,
            })

        if not players_cmd_opts:
            next_player = listeners[0]
            game_round.deal_cards_for_player(next_player, 1)
            cmd_opts = rule.get_player_cmd_options_for_cards(next_player, [], True, False)
            if not cmd_opts:
                cmd_opts.append(PlayCmd(next_player, InterProtocol.majiang_player_act_play_card))
            PlayMajiang.send_player_cmd_options(game_round, next_player, cmd_opts, cmd_opts[0])
        else:
            PlayMajiang.process_prioritized_player_cmds(players_cmd_opts, listeners[0])

    @staticmethod
    def process_prioritized_player_cmds(opt_players_cmds, next_player):
        if len(opt_players_cmds) == 1:
            if opt_players_cmds[0]["player"] == next_player:
                opt_players_cmds[0].cmds.append(PlayCmd(InterProtocol.majiang_player_act_mopai))
            else:
                opt_players_cmds[0].cmds.append(PlayCmd(InterProtocol.majiang_player_act_pass))
        elif len(opt_players_cmds) > 1:
            prioritized_cmds = []
            for i in range(0, len(InterProtocol.majiang_acts_priorities)):
                p_cmd = InterProtocol.majiang_acts_priorities[i]
                player = PlayMajiang.get_player_with_opt_cmd(opt_players_cmds, p_cmd)
                if player:
                    prioritized_cmds.append(player)

            if prioritized_cmds[-1]["player"] == next_player: # merge commands
                prioritized_cmds[-1]["cmds"].append(PlayCmd(next_player, InterProtocol.majiang_player_act_mopai))
            else:
                cmds = []
                cmds.append(PlayCmd(next_player, InterProtocol.majiang_player_act_mopai))
                prioritized_cmds.append({"player":next_player, "cmds":cmds})

    @staticmethod
    def get_player_with_opt_cmd(opt_players_cmds, test_opt_cmd):
        for p in opt_players_cmds:
            for c in p["cmds"]:
                if c.get_cmd() == test_opt_cmd:
                    return p

    @staticmethod
    def on_player_selected_action(game_round, player, cmd, cmd_data = None, silent_cmd = False):
        if cmd == InterProtocol.majiang_player_act_peng:
            card = cmd_data
            game_round.player_select_peng(player, card)
            # PlayMajiang.send_player_cmd_options(game_round, player, [], True, False)
            cmd_opts = []
            play_card = PlayCmd(player, InterProtocol.majiang_player_act_play_card)
            play_card.set_cmd_param(player.get_active_cards()[0])
            cmd_opts.append(play_card)
            PlayMajiang.send_player_cmd_options(game_round, player, cmd_opts, cmd_opts[0])
        elif cmd == InterProtocol.majiang_player_act_gang:
            card = cmd_data
            game_round.player_select_gang(player, card)
            cmd_opts = []
            play_card = PlayCmd(player, InterProtocol.majiang_player_act_play_card)
            play_card.set_cmd_param(player.get_active_cards()[0])
            cmd_opts.append(play_card)
            PlayMajiang.send_player_cmd_options(game_round, player, cmd_opts, cmd_opts[0])
        elif cmd == InterProtocol.majiang_player_act_pass:
            pass
        elif cmd == InterProtocol.majiang_player_act_mopai:
            pass
            # in the case, the player give up the peng
            # the next player get chance to fetch one new card
            # starter = game_round.get_cur_play_starter()
            # listeners = game_round.get_one_play_listeners(starter)
            # next_player = listeners[0]
            # game_round.deal_cards_for_player(next_player, 1)
            # PlayMajiang.send_player_cmd_options(game_round, next_player, [], True, False)
        elif cmd == InterProtocol.majiang_player_act_hu:
            game_round.set_winners([player])
            game_round.test_and_update_current_stage()
        elif cmd == InterProtocol.majiang_player_act_play_card:
            PlayMajiang.on_one_card_played_out(game_round, player, cmd_data)
