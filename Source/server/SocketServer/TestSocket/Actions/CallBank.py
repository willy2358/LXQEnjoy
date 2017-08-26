from Actions.ActionBase import ActionBase


class CallBank(ActionBase):
    def __init__(self, text, act_id):
        super(CallBank, self).__init__(text, act_id)

    def execute(self):
        player = self.get_my_player()
        game_round = self.get_my_round()
        if player and game_round:
            game_round.set_bank_player(player)
