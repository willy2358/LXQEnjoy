from GCore.Statement import Statement
from GCore.Elements.Ret import Ret
from GCore.Elements.Variable import Variable
from GCore.Elements.Loop import Loop
import Mains.Log as Log

# <proc name="proc_example" params="#player,#cards">
# note: 在proc内部定义的局部变量需以#打头，表示局部变量，在变量命名上尽量加上本proc的前缀。
# 因为变量都共享一个PlayScene.__local_var局部变量命名空间，尽量减小从命名上减小干扰。
class Proc(Statement):
    def __init__(self, name, params):
        super(Proc, self).__init__()
        self.__name = name
        self.__params = params
        self.__statements = []

    def get_name(self):
        return self.__name

    def get_params(self):
        return self.__params

    def get_param_names(self):
        names = []
        if isinstance(self.__params, list):
            for p in self.__params:
                # p is Varible
                names.append(p.get_name())
        return names

    def add_statement(self, stm):
        self.__statements.append(stm)

    def gen_runtime_obj(self, scene):
        # varibles, register in scene
        if self.__params:
            for p in self.__params:
                p.gen_runtime_obj(scene)(self.__name)

        def proc_func():
            bakCtx = scene.get_cur_proc_rtx()
            try:
                Log.debug("Executing:{0} ....".format(self.get_step()))
                rtObjs = []
                for c in self.__statements:
                    # this ctx will ge overridden by inner calling proc
                    scene.set_cur_proc_ctx(self.__name)
                    if isinstance(c, Ret):
                        return scene.get_obj_value(c.gen_runtime_obj(scene))
                    func = None
                    if isinstance(c, Loop):
                        func = c.gen_runtime_no_pause_obj(scene)
                    else:
                        func = c.gen_runtime_obj(scene)
                    if callable(func):
                        if isinstance(c, Variable):
                            func(self.__name)
                        else:
                            func()
            except Exception as ex:
                Log.exception(ex)
            finally:
                scene.set_cur_proc_ctx(bakCtx)
        return proc_func


