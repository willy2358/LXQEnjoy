class PatternModes(object):
    """description of class"""
    def __init__(self, name, score=0, **kwargs):
        self.__name = name
        self.__score = score
        self.__modes = []
        return super().__init__(**kwargs)

    def add_mode(self, mode):
        self.__modes.append(mode)

    def set_score(self, score):
        self.__score = score

    def get_score(self):
        return self.__score

    def get_name(self):
        return self.__name

    def is_match(self, faces):
        for m in self.__modes:
            if not m.is_match(faces):
                return False
        return True
