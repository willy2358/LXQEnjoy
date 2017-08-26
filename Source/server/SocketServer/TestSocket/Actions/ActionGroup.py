class ActionGroup:
    def __init__(self):
        self.__actions = []
        self.__default_action = None
        self.__player_select_timeout_seconds = 20

    def get_action_by_id(self, action_id):
        for a in self.__actions:
            a = a.find_follow_action_from_id(action_id)
            if a:
                return a

        return None

    def get_actions(self):
        return self.__actions

    def get_select_timeout(self):
        return self.__player_select_timeout_seconds

    def get_default_action(self):
        return self.__default_action

    def set_default_action(self, action):
        self.__default_action = action

    def set_select_timeout(self, seconds):
        self.__player_select_timeout_seconds = seconds

    def add_action(self, action, is_default_action=False):
        if action:
            self.__actions.append(action)
        if is_default_action:
            self.__default_action = action
        return action

    def to_json_object(self):
        if self.__actions and self.__default_action:
            acts = [act.to_json_object() for act in self.__actions]
            return {"actions": acts, "default": self.__default_action.to_json_object()}
        else:
            return None