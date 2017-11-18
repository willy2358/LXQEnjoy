from GameStages.GameStage import GameStage

import InterProtocol


# terms: one-play: includes:
# letting one player play one card, this play is called the starter
# this player played one card
# letting other players response to the played card, these players are called listeners
# one listener got the played card or got a new card from table
# this listener become the starter of new one-play, new one-play begins
class PlayMajiang(GameStage):
    def __init__(self):
        pass

    @staticmethod
    def execute(game_round):
        rule = game_round.get_rule()
        starter = game_round.get_bank_player()
        # PlayMajiang.begin_one_play(game_round, starter)
        cmd_opts = rule.get_player_cmd_options_for_cards(starter, [], False, False)
        packet = InterProtocol.create_cmd_options_json_packet(cmd_opts)
        starter.send_server_command(packet)

    @staticmethod
    def is_ended_in_round(game_round):
        winners = game_round.get_winners()
        if len(winners) > 0:
            return True
        else:
            return False

    @staticmethod
    def begin_one_play(game_round, starter):
        rule = game_round.get_rule()
        cmd_opts = rule.get_cmd_options_for_cards(starter.get_in_hand_cards())
        packet = InterProtocol.create_cmd_options_json_packet(cmd_opts)
        starter.send_server_command(packet)

    @staticmethod
    def on_one_card_played_out(game_round, player, played_card):
        listeners = game_round.get_one_play_listeners(player)
        rule = game_round.get_rule()
        waiting_player_act = False
        for p in listeners:
            cmd_opts = rule.get_player_cmd_options_for_cards(p, [played_card], p == listeners[0], True)
            if len(cmd_opts) > 0:
                packet = InterProtocol.create_cmd_options_json_packet(cmd_opts)
                p.send_server_command(packet)
                waiting_player_act = True

        if not waiting_player_act:
            next_player = listeners[0]
            game_round.deal_cards_for_player(next_player, 1)
            game_round.set_one_player_starter(next_player)
            PlayMajiang.begin_one_play(game_round, next_player)

    @staticmethod
    def on_player_selected_action(game_round, player, cmd, cmd_data):
        if cmd == InterProtocol.majiang_player_act_peng:
            card = cmd_data
            game_round.player_select_peng(player, card)
            game_round.set_one_player_starter(player)
            PlayMajiang.begin_one_play(game_round, player)
        elif cmd == InterProtocol.majiang_player_act_gang:
            card = cmd_data
            game_round.player_select_gang(player, card)
            game_round.set_one_player_starter(player)
            PlayMajiang.begin_one_play(game_round, player)
        elif cmd == InterProtocol.majiang_player_act_pass\
                or cmd == InterProtocol.majiang_player_act_new_card:
            # in the case, the player give up the peng
            # the next player get chance to fetch one new card
            starter = game_round.get_cur_play_starter()
            listeners = game_round.get_one_play_listeners(starter)
            next_player = listeners[0]
            game_round.deal_cards_for_player(next_player, 1)
            PlayMajiang.begin_one_play(game_round, next_player)
        elif cmd == InterProtocol.majiang_player_act_hu:
            game_round.set_winners([player])
