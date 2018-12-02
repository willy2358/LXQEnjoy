
from GCore.Operation import Operation

class Operand(Operation):
    def __init__(self, code):
        super(Operand, self).__init__(None, None, None)
        self.__code = code

