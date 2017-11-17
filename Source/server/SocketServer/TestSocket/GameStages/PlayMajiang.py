from GameStages.GameStage import GameStage

import InterProtocol


class PlayMajiang(GameStage):
    def __init__(self, rule):
        super(PlayMajiang, self).__init__(rule)

    # terms: one-play: includes:
    # letting one player play one card, this play is called the starter
    # this player played one card
    # letting other players response to the played card, these players are called listeners
    # one listener got the played card or got a new card from table
    # this listener become the starter of new one-play, new one-play begins
    @staticmethod
    def execute(game_round):
        rule = game_round.get_rule()
        starter = game_round.get_bank_player()
        PlayMajiang.begin_one_play(game_round, starter)

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
        player_can_get_card = False
        for p in listeners:
            cmd_opts = rule.get_cmd_options_for_cards(p.get_in_hand_cards() + [played_card])
            if len(cmd_opts) > 0:
                packet = InterProtocol.create_cmd_options_json_packet(cmd_opts)
                p.send_server_command(packet)
                player_can_get_card = True

        if not player_can_get_card:
            game_round.deal_cards_for_player(listeners[0], 1)
            game_round.set_one_player_starter(listeners[0])
            PlayMajiang.begin_one_play(game_round, listeners[0])

    @staticmethod
    def on_player_cmd_action(game_round, player, cmd, cmd_data):
        if cmd == InterProtocol.majiang_player_act_peng:
            card = 111
            player.add_pend_card(card)
            game_round.set_one_player_starter(player)
            PlayMajiang.begin_one_play(game_round, player)
        elif cmd == InterProtocol.majiang_player_act_pass:
            # in the case, the non-next player give up the peng
            # the next player get chance to fetch one new card
            starter = game_round.get_cur_play_starter()
            listeners = game_round.get_one_play_listeners(starter)
            next_player = listeners[0]
            game_round.deal_cards_for_player(next_player, 1)
            PlayMajiang.begin_one_play(game_round, next_player)

        #banker
        #push cmd to let banker play one card or hu
        #listen player playing card event
        #if one player can peng
           #push to let player peng or pass
        #else
           #deal a new card to next player
