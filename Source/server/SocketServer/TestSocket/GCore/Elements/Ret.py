from GCore.Statement import Statement
# <ret value="2"></ret> / <ret value="@var"></ret>
# note: ret 节点不能位于ift 节点内
class Ret(Statement):
    def __init__(self, ret_val):
        self.__ret_val = ret_val

    def get_ret_value(self):
        return self.__ret_val

    def gen_runtime_obj(self, scene):
        def ret_func():
            return self.__ret_val.gen_runtime_obj(scene)
        return ret_func

