from Actions.ActionGroup import ActionGroup


class GameStage:
    def __init__(self, rule):
        self.__my_rule = rule
        self.__my_round = None
        self.__my_players = None
        self.__head_action_group = None

    def get_my_rule(self):
        return self.__my_rule

    def get_my_round(self):
        return self.__my_round

    def get_my_players(self):
        return self.__my_players

    def get_head_action_group(self):
        return self.__head_action_group

    def get_action_by_id(self, action_id):
        head_group = self.get_head_action_group()
        if head_group:
            return head_group.get_action_by_id(action_id)
        else:
            return None

    def set_my_round(self, my_round):
        self.__my_round = my_round
        self.__my_players = self.__my_round.get_players()

    def add_player_action(self, action, as_default_action=False):
        if not self.__head_action_group:
            self.__head_action_group = ActionGroup()
        self.__head_action_group.add_action(action, as_default_action)

    def begin(self):
        pass

    def continue_execute(self):
        pass

    def process_player_selected_action_id(self, action_id):
        pass
