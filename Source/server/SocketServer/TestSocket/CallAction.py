

class CallAction:
    def __init__(self, action_id, cmd_text):
        self.__action_id = action_id
        self.__cmd_text = cmd_text
        self.__follow_up_actions = []

    def add_follow_up_action(self, action):
        self.__follow_up_actions.append(action)
        return action

    def get_follow_up_actions(self):
        return self.__follow_up_actions

    def get_action_id(self):
        return self.__action_id

    def to_json(self):
        return '{{"action_id":"{0}","action_text":"{1}"}}'.format(self.__action_id, self.__cmd_text)

    def get_follow_up_actions_of_action(self, action_id):
        if self.get_action_id() == action_id:
            return self.__follow_up_actions

        for act in self.__follow_up_actions:
            if act.get_action_id() == action_id:
                return act.get_follow_up_actions()
            else:
                acts = act.get_follow_up_actions_of_action(act.get_action_id())
                if acts:
                    return acts

        return None
