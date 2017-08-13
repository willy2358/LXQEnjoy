from GameStages.GameStage import GameStage


class CallBanker(GameStage):
    def __init__(self, rule):
        super(CallBanker, self).__init__(rule)

    def is_completed(self):
        return False

    def begin(self):
        pass

