from GCore.Statement import Statement
from GCore.Elements.Ret import Ret
import Mains.Log as Log

# <proc name="proc_example" params="#player,#cards">
# note: 在proc内部定义的局部变量需以#打头，表示局部变量，在变量命名上尽量加上本proc的前缀。
# 因为变量都共享一个PlayScene.__local_var局部变量命名空间，尽量减小从命名上减小干扰。
class Proc(Statement):
    def __init__(self, name):
        self.__name = name
        self.__statements = []

    def get_name(self):
        return self.__name

    def add_statement(self, stm):
        self.__statements.append(stm)

    def gen_runtime_obj(self, scene):
        def proc_func():
            try:
                rtObjs = []
                for c in self.__statements:
                    if isinstance(c, Ret):
                        return scene.get_obj_value(c.get_ret_value())
                    func = c.gen_runtime_obj(scene)
                    if callable(func):
                        func()
            except Exception as ex:
                Log.exception(ex)
        return proc_func


