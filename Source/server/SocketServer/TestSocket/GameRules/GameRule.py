class GameRule:
    def __init__(self, rule_id):
        self.__player_num_min = 0;
        self.__player_num_max = 0;
        # 设置底牌数
        self.__cards_num_not_deal = 0;
        self.__rule_id = rule_id;
        self.__cards = []
        # self.__stages = []
        self.__game_stages = []

        # self.__call_actions = []
        self.__head_action_group = ActionGroup()
        self.__player_idx_of_play_card = -1
        self.__cur_game_stage_idx = -1;

    def get_head_action_group(self):
        return self.__head_action_group

    def get_next_game_stage(self):
        self.__cur_game_stage_idx += 1
        if self.__cur_game_stage_idx < len(self.__game_stages):
            return self.__game_stages[self.__cur_game_stage_idx]
        else:
            return None

    @staticmethod
    def get_is_round_end(game_round):
        players = game_round.get_players()
        for p in players:
            if len(p.get_remained_cards()) < 1:
                return True

        return False

    @staticmethod
    def get_player_default_cards(player):
        rem_cards = player.get_remained_cards()
        if rem_cards and len(rem_cards):
            c = rem_cards[0]
            return c
        else:
            return None

    @staticmethod
    def get_winners_for_round(game_round):
        winners = []
        players = game_round.get_players()
        banker = game_round.get_bank_player()
        if len(banker.get_remained_cards()) < 1:
            winners.append(banker)
        else:
            for p in players:
                if p is not banker:
                    winners.append(p)

        return winners

    @staticmethod
    def get_losers_for_round(game_round):
        losers = []
        players = game_round.get_players()
        banker = game_round.get_bank_player()
        if len(banker.get_remained_cards()) > 0:
            losers.append(banker)
        else:
            for p in players:
                if p is not banker:
                    losers.append(p)

        return losers

    def get_game_stages(self):
        return self.__game_stages

    def get_player_min_number(self):
        return self.__player_num_min

    def get_player_max_number(self):
        return self.__player_num_max

    def get_rule_id(self):
        return self.__rule_id

    def get_cards(self):
        return self.__cards

    def get_play_card_command_options(self, player):
        return ["play", "not-play"]

    @staticmethod
    def get_play_cards_commands_for_player(player, game_round):
        if not player or not game_round:
            return None
        dealer = game_round.get_my_dealer()
        if not dealer:
            return None
        act_group = ActionGroup()
        pre_player, pre_cards = dealer.get_previous_played_cards()
        if not pre_player or pre_player is player:
            play_card = PlayCard("Play cards", "1")
            play_card.set_execute_context(player, game_round)
            play_card.set_cards(GameRule.get_player_default_cards(player))
            act_group.add_action(play_card, True)
        else:
            play_card = PlayCard("Play cards", "1")
            play_card.set_execute_context(player, game_round)
            act_group.add_action(play_card)
            pass_play = PassPlay("Not Play", "2")
            pass_play.set_execute_context(player, game_round)
            act_group.add_action(pass_play, True)
        return act_group

    @staticmethod
    def order_play_card_players(play_round):
        players = play_round.get_players()
        banker = play_round.get_bank_player()
        if banker:
            idx = players.index(banker)
            ordered_players = players[idx:]
            for i in range(0,idx):
                ordered_players.append(players[i])
            return ordered_players
        else:
            pass

    def get_follow_up_action_group(self, action_id):
        if not action_id:
            return self.get_head_action_group()
        else:
            sub_act = self.get_head_action_group().get_action_by_id(action_id)
            if sub_act:
                return sub_act.get_following_action_group()
                # for act in self.get_head_action_group().get_actions():
                #     sub_act = act.find_action_from_id(action_id)
                #     if sub_act:
                #         return sub_act.get_follow_up_action_group()
        return None

    def get_action_by_id(self, action_id):
        return self.__head_action_group.get_action_by_id(action_id)

    def add_call_action(self, action):
        # self.__call_actions.append(action)
        self.__head_action_group.add_action(action)

    def set_player_min_number(self, number):
        self.__player_num_min = number

    def set_player_max_number(self, number):
        self.__player_num_max = number

    def set_cards_number_not_deal(self, number):
        self.__cards_num_not_deal = number

    def set_action_call_timeout_seconds(self, seconds):
        self.__head_action_group.set_select_timeout(seconds)

    def get_cards_number_not_deal(self):
        return self.__cards_num_not_deal

    def set_cards(self, cards):
        self.__cards = cards

    # def set_stages(self, stages):
    #     self.__stages = stages

    def add_game_stage(self, stage):
        self.__game_stages.append(stage)
