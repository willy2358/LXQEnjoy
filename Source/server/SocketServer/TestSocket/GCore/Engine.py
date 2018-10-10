from xml.dom.minidom import parse
import xml.dom.minidom

def ctype_of(card):
    return 'h'


def cfigure_of(card):
    return 12


def elem_of_index(array, index):
    return array[index]


def value_of(expr):
    return 1


def execute(expressions):
    pass

def is_attr_expression(attrValue):
    return True


def is_satisfy(argExpr1, argExpr2, op):
    if op == "ret_as" or op == "ret_is":
        return value_of(argExpr1) == value_of(argExpr2)

    if op == "ret_not_is" or op == "ret_not_is":
        return value_of(argExpr1) != value_of(argExpr2)

    if op == "ret_lt" or op == "ret_lt_as":
        return value_of(argExpr1) < value_of(argExpr2)

    if op == "ret_not_lt" or op == "ret_not_lt_as":
        return not (value_of(argExpr1) < value_of(argExpr2))

    if op == "ret_gt" or op == "ret_gt_as":
        return value_of(argExpr1) > value_of(argExpr2)

    if op == "ret_not_gt" or op == "ret_not_gt_as":
        return not (value_of(argExpr1) > value_of(argExpr2))


def Test1Case(argExpr1, argExpr2, op, retExprs):
    if is_satisfy(argExpr1, argExpr2, op):
        execute(retExprs)


def test_and(case1Expr1, case1Expr2, case1Op,
             case2Expr1, case2Expr2, case2Op,
             retExprs):
    if is_satisfy(case1Expr1, case1Expr2, case1Op) \
            and is_satisfy(case2Expr1, case2Expr2, case2Op):
        execute(retExprs)


def test_and(case1Expr1, case1Expr2, case1Op,
             case2Expr1, case2Expr2, case2Op,
             case3Expr1, case3Expr2, case3Op,
             retExprs):
    if is_satisfy(case1Expr1, case1Expr2, case1Op) \
            and is_satisfy(case2Expr1, case2Expr2, case2Op) \
            and is_satisfy(case3Expr1, case3Expr2, case3Op):
        execute(retExprs)


def test_or(case1Expr1, case1Expr2, case1Op,
            case2Expr1, case2Expr2, case2Op,
            retExprs):
    if is_satisfy(case1Expr1, case1Expr2, case1Op) \
            or is_satisfy(case2Expr1, case2Expr2, case2Op):
        execute(retExprs)


def test_or(case1Expr1, case1Expr2, case1Op,
            case2Expr1, case2Expr2, case2Op,
            case3Expr1, case3Expr2, case3Op,
            retExprs):
    if is_satisfy(case1Expr1, case1Expr2, case1Op) \
            or is_satisfy(case2Expr1, case2Expr2, case2Op) \
            or is_satisfy(case3Expr1, case3Expr2, case3Op):
        execute(retExprs)

def parse_case(xmlNode):
    pass

def parse_update(xmlNode):
    pass

def parse_clause(xmlNode):
    pass

