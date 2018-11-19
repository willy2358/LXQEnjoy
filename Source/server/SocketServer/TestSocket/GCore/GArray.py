
from GCore.Operand import Operand

class GArray(Operand):
    def __init__(self, elems):
        self.__elems = elems


    def gen_runtime_obj(self, scene):
        def ret_elems():
            elems = []
            for e in self.__elems:
                val = scene.get_obj_value(e)
                elems.append(val)
            return elems
        return ret_elems