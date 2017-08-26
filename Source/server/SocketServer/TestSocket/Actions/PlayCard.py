from Actions.ActionBase import ActionBase


class PlayCard(ActionBase):
    def __init__(self, text, act_id):
        super(PlayCard, self).__init__(text, act_id)
        self.__cards = None

    def set_cards(self, cards):
        self.__cards = cards

    def execute(self):
        player = self.get_my_player()
        if player and self.__cards and len(self.__cards) > 0:
            player.play_out_cards(self.__cards)
            dealer = self.get_my_round().get_my_dealer()
            dealer.record_player_cards_history(player, self.__cards)

    def to_broadcast_json_object(self):
        return {"act": "play-cards", "cards": self.__cards}