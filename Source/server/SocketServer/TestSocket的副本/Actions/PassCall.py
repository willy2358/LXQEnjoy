from Actions.ActionBase import ActionBase


class PassCall(ActionBase):
    def __init__(self, text, act_id):
        super(PassCall, self).__init__(text, act_id)

    def execute(self):
        pass

