from Actions.ActionBase import ActionBase


class PlayCard(ActionBase):
    def __init__(self, text, act_id):
        super(PlayCard, self).__init__(text, act_id)
