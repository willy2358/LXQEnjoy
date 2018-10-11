
from GCore.Operator import Operator

class Update:
    def __init__(self, targetObj, targetProp, opVal, op = Operator.Update):
        self.__targetObj = targetObj
        self.__targetProp = targetProp
        self.__op = op
        self.__opVal = opVal

    def execute(self):
        pass

