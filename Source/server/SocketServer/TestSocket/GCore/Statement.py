
class Statement:
    def __init__(self):
        self.__parent = None

    def get_target_property(self):
        pass

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent