from CardsPattern.Mode import Mode

class Mode_Single(Mode):

    """description of class"""
    def __init__(self, face):
        self.__face = face

    def is_match(self, faces):
        return self.__face in faces
