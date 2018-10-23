
from GCore.Operator import Operator
from GCore.Statement import Statement
from GCore.VarsSpace import *


class Operation(Statement):
    def __init__(self, operand1, operand2, operator = Operator.Add):
        self.__result_name = None
        self.__operator = operator
        self.__operand1 = operand1
        self.__operand2 = operand2
        self.__result_var_node = None
        self.__result_var_name = None
        self.__xmlNode = None

    def set_result_var(self, node, varName):
        self.__result_var_node = node
        self.__result_var_name = varName

    def set_xml_node(self, node):
        self.__xmlNode = node

    def get_result(self):
        var1 = self.__operand1.get_result()
        var2 = self.__operand2.get_result()
        ret = None
        if self.__operator == Operator.Add:
            ret = var1 + var2
        elif self.__operator == Operator.Subtract:
            ret = var1 - var2
        elif self.__operator == Operator.Multiply:
            ret = var1 * var2

        if self.__result_var_name and self.__result_var_node:
            update(self.__result_var_node, self.__result_var_name, ret)

        return ret