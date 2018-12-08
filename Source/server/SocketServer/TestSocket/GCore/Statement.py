
class Statement:
    def __init__(self):
        self.__parent = None
        self.__step = None

    def get_target_property(self):
        pass

    def get_step(self):
        if self.__step == "fk_2":
            stop = 1
        return self.__step

    def set_step(self, step):
        self.__step = step

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent

    def gen_runtime_obj(self, scene):
        return None
