from CardsPattern.Mode import Mode

class Mode_Pair(Mode):
    """description of class"""
    def __init__(self, face):
        self.__face = face

    
    def is_match(self, faces):
        for f in faces:
            if faces.count(f) == 2:
                return True

        return False
