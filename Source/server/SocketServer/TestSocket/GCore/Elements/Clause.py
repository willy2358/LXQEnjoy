
from GCore.Operator import Operator
from GCore.Statement import Statement

class Clause(Statement):
    def __init__(self, Op = Operator.And):
        self.__case = None
        self.__true_statements = []
        self.__false_statements = []

    def get_true_statements(self):
        return self.__true_statements

    def get_false_statements(self):
        return self.__false_statements

    def set_case(self, case):
        if case:
            self.__case = case

    def add_true_statement(self, update):
        self.__true_statements.append(update)

    def add_false_statement(self, update):
        self.__false_statements.append(update)

    def set_true_statements(self, updates):
        self.__true_statements = updates

    def set_false_statements(self, updates):
        self.__false_statements = updates


    def execute(self):
        if self.__case is not None and self.__case.is_satisfy():
            for u in self.__true_statements:
                u.execute()

    def gen_true_runtime_objs(self, scene):
        if not self.__true_statements:
            return None
        objs = []
        for stm in self.__true_statements:
            rtObj = stm.gen_runtime_obj()
            if rtObj:
                objs.append(rtObj)
        return objs

    def gen_false_runtime_objs(self, scene):
        if not self.__false_statements:
            return None
        objs = []
        for stm in self.__false_statements:
            rtObj = stm.gen_runtime_obj()
            if rtObj:
                objs.append(rtObj)
        return objs

    def gen_runtime_obj(self, scene):
        assert self.__case
        cond = self.__case.gen_runtime_obj
        if not cond:
            return None
        t_rt_objs = self.get_true_statements()
        f_rt_objs = self.get_false_statements()

        def if_test():
            if cond():
                if t_rt_objs:
                    for func in t_rt_objs:
                        func()
            else:
                if f_rt_objs:
                    for func in f_rt_objs:
                        func()

        return if_test

