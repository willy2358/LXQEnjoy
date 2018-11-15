
from GCore.Statement import Statement
import Mains.Log as Log

class Loop(Statement):
    def __init__(self):
        self.__exit_cond = None
        self.__clauses = []

    def get_clauses(self):
        return self.__clauses

    def get_exit_condition(self):
        return self.__exit_cond

    def set_exit_case(self, case):
        self.__exit_cond = case

    def add_clause(self, clause):
        self.__clauses.append(clause)

    def gen_runtime_obj(self, scene):
        assert self.__exit_cond

        loop_test = self.__exit_cond.gen_runtime_obj(scene)
        rtObjs = []
        for c in self.__clauses:
            obj = c.gen_runtime_obj(scene)
            if obj:
                rtObjs.append(obj)

        def sub_proc():
            try:
                while loop_test():
                    for func in rtObjs:
                        if callable(func):
                            func()
            except Exception as ex:
                Log.exception(ex)
        return sub_proc

