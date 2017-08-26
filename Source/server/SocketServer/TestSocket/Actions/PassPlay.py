from Actions.ActionBase import ActionBase


class PassPlay(ActionBase):
    def __init__(self, text, act_id):
        super(PassPlay, self).__init__(text, act_id)

    def execute(self):
        pass

