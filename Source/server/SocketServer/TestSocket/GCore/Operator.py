
from enum import Enum
import GCore.Engine
from GCore.Engine import *

class Operator(Enum):
    Unknown = 0
    And = 1
    Or = 2
    Not = 3

    Add = 4
    Subtract = 5
    Multiply = 6

    Equal = 7
    NotEqual = 8
    LessThan = 9
    NotLessThan = 10
    GreaterThan = 11
    NotGreaterThan = 12

    Update = 100


def from_str(strOp):
    if strOp == GCore.Engine.attr_name_ret_as or strOp == GCore.Engine.attr_name_ret_is:
        return Operator.Equal
    elif strOp == GCore.Engine.attr_name_ret_not_is or strOp == GCore.Engine.attr_name_ret_not_as:
        return Operator.NotEqual
    elif strOp == GCore.Engine.attr_name_ret_lt or strOp == GCore.Engine.attr_name_ret_lt_as:
        return Operator.LessThan
    elif strOp == GCore.Engine.attr_name_ret_not_lt or strOp == GCore.Engine.attr_name_ret_not_lt_as:
        return Operator.NotLessThan
    elif strOp == GCore.Engine.attr_name_ret_gt or strOp == GCore.Engine.attr_name_ret_gt_as:
        return Operator.GreaterThan
    elif strOp == GCore.Engine.attr_name_ret_not_gt or strOp == GCore.Engine.attr_name_ret_not_gt_as:
        return Operator.NotGreaterThan
    elif strOp == GCore.Engine.attr_val_op_and or strOp == "##":
        return Operator.And
    elif strOp == GCore.Engine.attr_val_op_or or strOp == "||":
        return Operator.Or
    elif strOp == GCore.Engine.attr_val_op_not:
        return Operator.Not
    elif strOp == GCore.Engine.attr_val_op_add:
        return Operator.Add
    elif strOp == GCore.Engine.attr_val_op_subtract:
        return Operator.Subtract
    elif strOp == GCore.Engine.attr_val_op_multiply:
        return Operator.Multiply
    else:
        return Operator.Unknown
