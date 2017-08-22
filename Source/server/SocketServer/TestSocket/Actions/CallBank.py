from Actions.ActionBase import ActionBase


class CallBank(ActionBase):
    def __init__(self, text, act_id):
        super(CallBank, self).__init__(text, act_id)