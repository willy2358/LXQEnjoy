from GameStages.GameStage import GameStage

import InterProtocol

class PublishScores(GameStage):
    def __init__(self, rule):
        super(PublishScores, self).__init__(rule)

    @staticmethod
    def execute(game_round):
        room = game_round.get_my_room()
        if room:
            for p in game_round.get_players():
                room.update_player_total_score(p)
            pack = InterProtocol.create_players_total_score_in_room(room)
            game_round.publish_round_states(pack)

        else:
            pack = InterProtocol.create_players_total_score_in_round(game_round)
            game_round.publish_round_states(pack)

        game_round.set_final_scores_published()

    @staticmethod
    def is_ended_in_round(game_round):
        return game_round.get_is_final_scores_published()