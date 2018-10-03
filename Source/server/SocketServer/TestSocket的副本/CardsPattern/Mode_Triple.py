from CardsPattern.Mode import Mode

class Mode_Triple(Mode):
    """description of class"""
    def __init__(self, face):
        self.__face = face

    def is_match(self, faces):
        return faces.count(self.__face) == 3


