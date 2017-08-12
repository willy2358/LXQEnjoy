#coding=utf-8


class ActionGroup:
    def __init__(self):
        self.__actions = []
        self.__player_select_timeout_seconds = 5

    def get_actions(self):
        return self.__actions

    def get_action_by_id(self, action_id):
        for a in self.__actions:
            a = a.find_action_from_id(action_id)
            if a:
                return a

        return None

    def get_select_timeout(self):
        return self.__player_select_timeout_seconds

    def add_action(self, action):
        self.__actions.append(action)

    def set_select_timeout(self, seconds):
        self.__player_select_timeout_seconds = seconds

    def to_json(self):
        j_str = '{"actions":['
        for c in self.__actions:
            j_str += c.to_json() + ","
        j_str += "]}"

        return j_str

    def get_default_action(self):
        for c in self.__actions:
            if c.get_is_default():
                return c
        return None


