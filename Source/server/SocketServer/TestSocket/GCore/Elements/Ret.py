from GCore.Statement import Statement
import Mains.Log as Log
# <ret value="2"></ret> / <ret value="@var"></ret>
# note: ret 节点不能位于ift 节点内
class Ret(Statement):
    def __init__(self, ret_val):
        super(Ret, self).__init__()
        self.__ret_val = ret_val

    def get_ret_value(self):
        return self.__ret_val

    def gen_runtime_obj(self, scene):
        def ret_func():
            Log.debug("Executing:{0} ....".format(self.get_step()))
            return self.__ret_val.gen_runtime_obj(scene)
        return ret_func

