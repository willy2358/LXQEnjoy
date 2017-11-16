
from GameStages import GameStage


class DealMaJiangs(GameStage):
    def __init__(self, rule):
        super(DealMaJiangs, self).__init__(rule)

    @staticmethod
    def execute(game_round):
        rule = game_round.get_rule()
        banker_cards_num = rule.get_cards_number_for_banker()
        player_cards_num = rule.get_cards_number_for_non_banker()
        for p in game_round.get_players():
            if p.is_banker():
                game_round.deal_cards_for_player(p, banker_cards_num)
            else:
                game_round.deal_cards_for_player(p, player_cards_num)

    def is_completed(self):
        return self.__cards_sent

    def begin(self):
        # cards = self.get_my_rule().get_cards()
        # cards_b = cards[:]  # copy this list
        # remain_cards = random.sample(cards_b, self.get_my_rule().get_cards_number_not_deal())
        # self.get_my_round().set_cards_for_banker(remain_cards[:])
        # Utils.list_remove_parts(cards_b, remain_cards)
        # players = self.get_my_round().get_players()
        # player_num = len(players)
        # for p in players:
        #     p.begin_new_deal()
        # while len(cards_b) > 0:
        #     cards_one_deal = random.sample(cards_b, player_num)
        #     for j in range(player_num):
        #         cmd_obj = {"cmd": DealCards.COMMAND_DEAL_CARD, "cards": [cards_one_deal[j]]}
        #         players[j].add_dealed_cards(cards_one_deal[j])
        #         players[j].send_server_command(cmd_obj)
        #         # players[j].deal_one_card(cards_one_deal[j])
        #     Utils.list_remove_parts(cards_b, cards_one_deal)
        # for p in players:
        #     p.finish_new_deal()
        #
        # self.__cards_sent = True
        # self.get_my_round().test_and_update_current_stage()
        pass

    def continue_execute(self):
        pass