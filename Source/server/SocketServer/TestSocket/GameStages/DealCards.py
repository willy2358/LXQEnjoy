import random

import Utils
from GameStages.GameStage import GameStage


class DealCards(GameStage):
    def __init__(self, rule):
        super(DealCards, self).__init__(rule)

    def is_completed(self):
        return False

    def begin(self):
        cards = self.get_my_rule().get_cards()
        cards_b = cards[:]  # copy this list
        remain_cards = random.sample(cards_b, self.get_my_rule().get_cards_number_not_deal())
        Utils.list_remove_parts(cards_b, remain_cards)
        players = self.get_my_round().get_players()
        player_num = len(players)
        for p in players:
            p.begin_new_deal()
        while len(cards_b) > 0:
            cards_one_deal = random.sample(cards_b, player_num)
            for j in range(player_num):
                players[j].deal_one_card(cards_one_deal[j])
            Utils.list_remove_parts(cards_b, cards_one_deal)
        for p in players:
            p.finish_new_deal()