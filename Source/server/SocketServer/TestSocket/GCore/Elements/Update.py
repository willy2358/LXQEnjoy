
from GCore.Operator import Operator
from GCore.Statement import Statement
from GCore.Engine import *
import GCore.Engine

# <update property="@bank_cfigure" op="add" value="1"/>
# <update property="IsMainPlayer" value="true"/>
class Update(Statement):
    def __init__(self, target, opVal, op = Operator.Update):
        if not GCore.Engine.is_var_ref(target):
            raise Exception("should be a variable, start with @")
        # ps = target.split('.')
        # assert len(ps) >= 2, "at least two parts, seperated by dot"
        self.__target = target
        # self.__targetObj = target[0:-(len(self.__targetProp) + 1)]
        self.__op = op
        self.__opVal = opVal

    def get_target_property(self):
        return self.__target

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
