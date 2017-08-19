from ActionGroup import ActionGroup


class CallAction:
    def __init__(self, action_id, cmd_text):
        self.__action_id = action_id
        self.__cmd_text = cmd_text
        self.__follow_up_actions = []
        self.__is_default = False
        self.__timeout_seconds = 10
        self.__following_action_group = None
        self.__is_bank_action = False
        self.__is_ending = False

    def add_follow_up_action(self, action):
        # self.__follow_up_actions.append(action)
        if not self.__following_action_group:
            self.__following_action_group = ActionGroup()

        self.__following_action_group.add_action(action)
        return action

    def get_follow_up_actions(self):
        if self.__following_action_group:
            return self.__following_action_group.get_actions()
        # return self.__follow_up_actions

    def get_action_id(self):
        return self.__action_id

    def get_is_ending(self):
        return self.__is_ending

    def get_is_bank_action(self):
        return self.__is_bank_action

    def get_following_action_group(self):
        return self.__following_action_group

    def set_as_default(self):
        self.__is_default = True

    def set_is_ending(self):
        self.__is_ending = True

    def set_is_bank_action(self):
        self.__is_bank_action = True

    def set_timeout_seconds(self, seconds):
        self.__timeout_seconds = seconds

    def to_json(self):
        return '{{"action_id":"{0}","action_text":"{1}"}}'.format(self.__action_id, self.__cmd_text)

    def get_follow_up_actions_of_action(self, action_id):
        if self.get_action_id() == action_id:
            return self.__follow_up_actions

        for act in self.__follow_up_actions:
            if act.get_action_id() == action_id:
                return act.get_follow_up_action_group()
            else:
                acts = act.get_follow_up_actions_of_action(act.get_action_id())
                if acts:
                    return acts

        return None

    def find_action_from_id(self, action_id):
        if self.get_action_id() == action_id:
            return self

        if self.__following_action_group:
            for a in self.__following_action_group.get_actions():
                sub_a = a.find_action_from_id(action_id)
                if sub_a:
                    return sub_a
        return None

    def get_is_default(self):
        return self.__is_default

    def get_timeout_seconds(self):
        return self.__timeout_seconds

