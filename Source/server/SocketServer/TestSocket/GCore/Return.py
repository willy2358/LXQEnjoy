from GCore.Operand import Operand

class Return(Operand):
    def __init__(self, var):
        self.__var = var


    def gen_runtime_obj(self, scene):
        def var_ref():
            return scene.get_obj_value(self.__var)

        return var_ref