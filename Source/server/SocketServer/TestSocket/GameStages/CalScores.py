from GameStages.GameStage import GameStage


class CalScores(GameStage):
    def __init__(self, rule):
        super(CalScores, self).__init__(rule)

    def is_completed(self):
        return False

    def begin(self):
        pass

    def continue_execute(self):
        pass
