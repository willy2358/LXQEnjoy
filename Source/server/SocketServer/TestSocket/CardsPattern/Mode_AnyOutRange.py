from CardsPattern.Mode import Mode

class Mode_AnyOutRange(Mode):
    """description of class"""

    def __init__(self, start, end, **kwargs):
        self.__start = start
        self.__end = end
        return super().__init__(**kwargs)

    def is_match(self, faces):
        for f in faces:
            if f < self.__start or f > self.__end:
                return True

        return True