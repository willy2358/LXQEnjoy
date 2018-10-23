
from GCore.Operator import Operator
from GCore.Statement import Statement
from GCore.Engine import *
import GCore.Engine

class Update(Statement):
    def __init__(self, targetObj, targetProp, opVal, op = Operator.Update):
        self.__targetObj = targetObj
        self.__targetProp = targetProp
        self.__op = op
        self.__opVal = opVal
        self.__case = None

    def __init__(self, target, opVal, op = Operator.Update):
        if not GCore.Engine.is_var_ref(target):
            raise Exception("should be a variable, start with @")
        ps = target.split('.')
        assert len(ps) >= 2, "at least two parts, seperated by dot"
        self.__targetProp = ps[-1]
        self.__targetObj = target[0:-(len(self.__targetProp) + 1)]
        self.__op = op
        self.__opVal = opVal

    def get_target_property(self):
        return self.__targetProp

    def execute(self):
        pass

    def set_exe_case(self, case):
        self.__case = case
