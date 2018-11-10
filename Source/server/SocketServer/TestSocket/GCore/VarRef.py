from GCore.Operand import Operand

class VarRef(Operand):
    def __init__(self, var):
        self.__var = var


    def gen_runtime_obj(self, scene):
        def var_ref():
            return scene.get_runtime_objs(self.__var)

        return var_ref
