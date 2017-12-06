from GameStages.PlayInTurn import PlayInTurn
from PlayCmd import PlayCmd
import InterProtocol
from GameRules.GameRule_Majiang import WinType


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
    def get_player_default_play_card(player):
        card = player.get_active_cards()[0]
        return card

    @staticmethod
    def execute(game_round):
        rule = game_round.get_rule()
        starter = game_round.get_bank_player()
        cmd_opts = rule.get_player_cmd_options_for_cards(starter, [], True, False)
        if not cmd_opts:
            def_cmd = PlayCmd(starter, InterProtocol.majiang_player_act_play_card)
            def_cmd.set_cmd_param(PlayMajiang.get_player_default_play_card(starter))
            cmd_opts.append(def_cmd)

        def_cmd = PlayMajiang.get_better_default_cmd_for_player(starter, cmd_opts, cmd_opts[0])
        game_round.send_player_cmd_options(starter, cmd_opts, def_cmd)

    @staticmethod
    def get_better_default_cmd_for_player(player, cmd_opts, default_opt):
        def_cmd = default_opt
        if player.get_is_robot_play():
            for c in cmd_opts:
                if c == InterProtocol.majiang_player_act_zimo or c == InterProtocol.majiang_player_act_hu:
                    def_cmd = c
                    break
        return def_cmd

    @staticmethod
    def is_ended_in_round(game_round):
        winners = game_round.get_winners()
        if len(winners) > 0:
            return True
        else:
            return False

    @staticmethod
    def on_one_card_played_out(game_round, player, played_card):
        listeners = game_round.get_one_play_listeners(player)
        rule = game_round.get_rule()
        players_cmd_opts = []
        for p in listeners:
            cmd_opts = rule.get_player_cmd_options_for_cards(p, [played_card], p == listeners[0], True)
            if cmd_opts:
                players_cmd_opts.append({
                    "player":p,
                    "cmds":cmd_opts,
                    "def-cmd":None
                })

        if not players_cmd_opts:
            next_player = listeners[0]
            game_round.deal_cards_for_player(next_player, 1)
            cmd_opts = rule.get_player_cmd_options_for_cards(next_player, [], True, False)
            if not cmd_opts:
                def_cmd = PlayCmd(next_player, InterProtocol.majiang_player_act_play_card)
                def_cmd.set_cmd_param(PlayMajiang.get_player_default_play_card(next_player))
                cmd_opts.append(def_cmd)
            def_cmd = PlayMajiang.get_better_default_cmd_for_player(next_player, cmd_opts, def_cmd)
            game_round.send_player_cmd_options(next_player, cmd_opts, def_cmd)
        else:
            PlayMajiang.process_prioritized_player_cmds(game_round, players_cmd_opts, listeners[0])

    @staticmethod
    def process_prioritized_player_cmds(game_round, opt_players_cmds, next_player):
        prioritized_cmds = []
        for i in range(0, len(InterProtocol.majiang_acts_priorities)):
            p_cmd = InterProtocol.majiang_acts_priorities[i]
            player = PlayMajiang.get_player_with_opt_cmd(opt_players_cmds, p_cmd)
            if player:
                prioritized_cmds.append(player)

        for i in range(0, len(prioritized_cmds)):
            if prioritized_cmds[i]["player"] != next_player:
                player = prioritized_cmds[i]["player"]
                pass_cmd = PlayCmd(player, InterProtocol.majiang_player_act_pass)
                prioritized_cmds[i]["cmds"].append(pass_cmd)
                cmd_opts = prioritized_cmds[i]["cmds"]
                def_cmd = PlayMajiang.get_better_default_cmd_for_player(player, cmd_opts, pass_cmd)
                prioritized_cmds[i]["def-cmd"] = def_cmd

            if i == len(prioritized_cmds) - 1:
                mopai_cmd = PlayCmd(next_player, InterProtocol.majiang_player_act_mopai)
                if prioritized_cmds[i]["player"] == next_player:  # merge commands
                    prioritized_cmds[i]["cmds"].append(mopai_cmd)
                    cmd_opts = prioritized_cmds[i]["cmds"]
                    def_cmd = PlayMajiang.get_better_default_cmd_for_player(next_player, cmd_opts, mopai_cmd)
                    prioritized_cmds[i]["def-cmd"] = def_cmd
                else:
                    cmds = [mopai_cmd]
                    prioritized_cmds.append({"player": next_player, "cmds": cmds, "def-cmd":mopai_cmd})

        game_round.start_process_for_players_want_played_out_cards(prioritized_cmds)

    @staticmethod
    def get_player_with_opt_cmd(opt_players_cmds, test_opt_cmd):
        for p in opt_players_cmds:
            for c in p["cmds"]:
                if c.get_cmd() == test_opt_cmd:
                    return p

    @staticmethod
    def on_player_selected_action(game_round, player, cmd, cmd_data = None, silent_cmd = False):
        pack = InterProtocol.create_player_exed_cmd_json_packet(player, cmd, cmd_data)
        game_round.publish_round_states(pack)

        if cmd == InterProtocol.majiang_player_act_peng:
            card = cmd_data
            game_round.player_select_peng(player, card)
            play_card = PlayCmd(player, InterProtocol.majiang_player_act_play_card)
            play_card.set_cmd_param(PlayMajiang.get_player_default_play_card(player))
            cmd_opts = [play_card]
            game_round.send_player_cmd_options(player, cmd_opts, cmd_opts[0])
        elif cmd == InterProtocol.majiang_player_act_gang:
            card = cmd_data
            game_round.player_select_gang(player, card)
            game_round.deal_cards_for_player(player, 1)
            cmd_opts = game_round.get_rule().get_player_cmd_options_for_cards(player, [], True, False)
            if not cmd_opts:
                play_card = PlayCmd(player, InterProtocol.majiang_player_act_play_card)
                play_card.set_cmd_param(PlayMajiang.get_player_default_play_card(player))
                cmd_opts = [play_card]
                game_round.send_player_cmd_options(player, cmd_opts, cmd_opts[0])
        elif cmd == InterProtocol.majiang_player_act_pass:
            game_round.move_next_pending_player_cmds()
        elif cmd == InterProtocol.majiang_player_act_mopai:
            game_round.deal_cards_for_player(player, 1)
            cmd_opts = game_round.get_rule().get_player_cmd_options_for_cards(player, [], True, False)
            def_cmd = None
            if not cmd_opts:
                play_card = PlayCmd(player, InterProtocol.majiang_player_act_play_card)
                play_card.set_cmd_param(PlayMajiang.get_player_default_play_card(player))
                cmd_opts = [play_card]
                def_cmd = play_card
            def_cmd = PlayMajiang.get_better_default_cmd_for_player(player,cmd_opts, cmd_opts[0])
            game_round.send_player_cmd_options(player, cmd_opts, def_cmd)
        elif cmd == InterProtocol.majiang_player_act_hu:
            losers = []
            card = cmd_data
            player.set_newest_cards([card],False, True)
            if game_round.get_rule().get_win_type() == WinType.dian_pao:
                losers.append(game_round.get_last_out_cards_player())
            else:
                for p in game_round.get_players():
                    if p != player:
                        losers.append(p)
            game_round.set_winners([player])
            game_round.set_losers(losers)
            game_round.test_and_update_current_stage()
        elif cmd == InterProtocol.majiang_player_act_zimo:
            losers = []
            card = cmd_data
            # player.set_newest_cards([card], True)
            for p in game_round.get_players():
                if p != player:
                    losers.append(p)

            game_round.set_winners([player])
            game_round.set_losers(losers)
            game_round.test_and_update_current_stage()
        elif cmd == InterProtocol.majiang_player_act_play_card:
            player.play_out_cards(cmd_data)
            game_round.record_last_out_cards(player, cmd_data)
            PlayMajiang.on_one_card_played_out(game_round, player, cmd_data)
