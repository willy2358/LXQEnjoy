
from GCore.Operand import Operand
from GCore.Operator import Operator
# find_player(IsDefender:true ## IsMainPlayer:true)  ## <==> &&
# find_player(IsDefender:true || IsMainPlayer:true)  || <==> ||
# filter_inst(@round.players, IsDefender:true ## IsMainPlayer:true)
class FuncCall(Operand):
    def __init__(self, funcName):
        self.__func_name = funcName
        self.__ordered_args = []
        self.__named_args = {}
        self.__named_arg_op = Operator.And

    def add_ordered_argument(self, arg):
        self.__ordered_args.append(arg)


    def add_named_argument(self, name, value):
        self.__named_args[name] = value

    def set_named_arg_operator(self, op=Operator.And):
        self.__named_arg_op = op



