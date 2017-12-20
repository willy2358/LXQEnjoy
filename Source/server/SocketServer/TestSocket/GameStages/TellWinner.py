from GameStages.GameStage import GameStage

import InterProtocol


class TellWinner(GameStage):
    def __init__(self, rule):
        super(TellWinner, self).__init__(rule)
        self.__executed = False

    def is_completed(self):
        return self.__executed

    def begin(self):
        rule = self.get_my_rule()
        winners = rule.get_winners_for_round(self.get_my_round())
        losers = rule.get_losers_for_round(self.get_my_round())
        for w in winners:
            msg = {"game-end": "won"}
            w.send_server_command(msg)
        for l in losers:
            msg = {"game-end": "lost"}
            l.send_server_command(msg)

        self.__executed = True

    def continue_execute(self):
        pass

    @staticmethod
    def execute(game_round):
        winners = game_round.get_winners()
        losers = game_round.get_losers()
        json_packet = InterProtocol.create_winners_losers_json_packet(winners, losers)
        for p in game_round.get_players():
            p.send_server_command(json_packet)


