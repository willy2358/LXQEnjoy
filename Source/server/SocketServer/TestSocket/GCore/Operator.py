
from enum import Enum

class Operator(Enum):
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


def from_str(strOp):
    if strOp == "ret_as" or strOp == "ret_is":
        return Operator.Equal
    elif strOp == "ret_not_is" or strOp == "ret_not_is":
        return Operator.NotEqual
    elif strOp == "ret_lt" or strOp == "ret_lt_as":
        return Operator.LessThan
    elif strOp == "ret_not_lt" or strOp == "ret_not_lt_as":
        return Operator.NotLessThan
    elif strOp == "ret_gt" or strOp == "ret_gt_as":
        return Operator.GreaterThan
    elif strOp == "ret_not_gt" or strOp == "ret_not_gt_as":
        return Operator.NotGreaterThan