from CardsPattern.Mode import Mode

class Mode_Seq(Mode):
    """description of class"""
    def __init__(self, start, count):
        self.__start = start
        self.__count = count

    
    def is_match(self, faces):
        for i in range(self.__start, self.__start + self.__count):
            if i not in faces:
                return False

        return True


