from GameStages.GameStage import GameStage


class TellWinner(GameStage):
    def __init__(self, rule):
        super(TellWinner, self).__init__(rule)

    def is_completed(self):
        return False

    def begin(self):
        pass

    def continue_execute(self):
        pass
