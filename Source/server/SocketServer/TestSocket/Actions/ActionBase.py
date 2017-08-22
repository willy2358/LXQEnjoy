

class ActionBase:
    def __init__(self, text, act_id):
        self.__act_text = text
        self.__act_id = act_id

    def get_act_text(self):
        return self.__act_text

    def set_act_text(self, text):
        self.__act_text = text

    def get_act_id(self):
        return self.__act_id

