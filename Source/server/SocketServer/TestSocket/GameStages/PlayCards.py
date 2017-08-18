from GameStages.GameStage import GameStage


class PlayCards(GameStage):
    def __init__(self, rule):
        super(PlayCards, self).__init__(rule)

    def is_completed(self):
        return False

    def begin(self):
        print("here i am")