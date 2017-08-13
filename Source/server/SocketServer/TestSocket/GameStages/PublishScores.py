from GameStages.GameStage import GameStage


class PublishScores(GameStage):
    def __init__(self, rule):
        super(PublishScores, self).__init__(rule)

    def is_completed(self):
        return False

    def begin(self):
        pass