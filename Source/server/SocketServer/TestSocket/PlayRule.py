from ActionGroup import ActionGroup


class PlayRule:
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

        self.__cur_game_stage_idx = -1;

    def get_head_action_group(self):
        return self.__head_action_group

    def get_next_game_stage(self):
        self.__cur_game_stage_idx += 1
        if self.__cur_game_stage_idx < len(self.__game_stages):
            return self.__game_stages[self.__cur_game_stage_idx]
        else:
            return None

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






