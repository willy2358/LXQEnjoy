from CardsPattern.Mode import Mode

class Mode_AnyInRange(Mode):
    """description of class"""
    def __init__(self, start, end, **kwargs):
        self.__start = start
        self.__end = end
        return super().__init__(**kwargs)

    def is_match(self, faces):
        for f in faces:
            if self.__start <= f <= self.__end:
                return True

        return False

