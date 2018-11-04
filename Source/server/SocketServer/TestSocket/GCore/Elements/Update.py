
from GCore.Operator import Operator
from GCore.Statement import Statement
from GCore.Engine import *
import GCore.Engine

class Update(Statement):
    # def __init__(self, target, targetProp, opVal, op = Operator.Update):
    #     self.__target = target
    #     # self.__targetProp = targetProp
    #     self.__op = op
    #     self.__opVal = opVal
    #     self.__case = None

    def __init__(self, target, opVal, op = Operator.Update):
        if not GCore.Engine.is_var_ref(target):
            raise Exception("should be a variable, start with @")
        # ps = target.split('.')
        # assert len(ps) >= 2, "at least two parts, seperated by dot"
        self.__target = target
        # self.__targetObj = target[0:-(len(self.__targetProp) + 1)]
        self.__op = op
        self.__opVal = opVal
        self.__case = None

    def get_target_property(self):
        return self.__target

    def execute(self):
        pass

    def set_exe_case(self, case):
        self.__case = case

    def get_result(self, originVal):
        if self.__op == Operator.Update:
            return self.__opVal
        elif self.__op == Operator.Add:
            return originVal + self.__opVal
        elif self.__operator == Operator.Subtract:
            return originVal - self.__opVal
        elif self.__operator == Operator.Multiply:
            return originVal * self.__opVal
        else:
            return originVal

    def gen_runtime_obj(self, scene):
        pass
