import random

import PlayManager
import Utils
from GameStages.GameStage import GameStage


class DealCards(GameStage):
    COMMAND_DEAL_CARD = "deal-cards"

    def __init__(self, rule):
        super(DealCards, self).__init__(rule)
        self.__cards_sent = False

    def is_completed(self):
        return self.__cards_sent
        # all_resp = True
        # players = self.get_my_round().get_players()
        # for p in players:
        #     if not p.has_received_resp("resp-" + PlayManager.SERVER_CMD_DEAL_FINISH):
        #         all_resp = False
        #         break;
        #
        # return all_resp

    def begin(self):
        cards = self.get_my_rule().get_cards()
        cards_b = cards[:]  # copy this list
        remain_cards = random.sample(cards_b, self.get_my_rule().get_cards_number_not_deal())
        self.get_my_round().set_cards_for_banker(remain_cards[:])
        Utils.list_remove_parts(cards_b, remain_cards)
        players = self.get_my_round().get_players()
        player_num = len(players)
        for p in players:
            p.begin_new_deal()
        while len(cards_b) > 0:
            cards_one_deal = random.sample(cards_b, player_num)
            for j in range(player_num):
                cmd_obj = {"cmd": DealCards.COMMAND_DEAL_CARD, "cards": [cards_one_deal[j]]}
                players[j].add_dealed_cards(cards_one_deal[j])
                players[j].send_server_command(cmd_obj)
                # players[j].deal_one_card(cards_one_deal[j])
            Utils.list_remove_parts(cards_b, cards_one_deal)
        for p in players:
            p.finish_new_deal()

        self.__cards_sent = True
        self.get_my_round().test_and_update_current_stage()

    def continue_execute(self):
        pass
