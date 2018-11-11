
from GCore.Operator import Operator
from GCore.Statement import Statement
from GCore.Engine import *
import GCore.Engine
from GCore.VarRef import VarRef

# <update property="@round.defenders" value="@scene.defenders"/>
# <update property="@drawer" value=":(next_player_of(@drawer))"/>
# <update property="@round.bank_ctype" value=":(var c; var t; c=max_cfigure_of(@round.kitty); t=ctype_of(@c); return @t)" />
# <update targets="@p1" property="IsMainPlayer" value="false"/>
# <update property="IsMainPlayer" targets=":(find_player(seatid == @seatid + 1))" value="true"/>
# <update targets=":(find_players(IsAttacter == true))" property="score" op="add" value="card_score"/>
class Update(Statement):
    def __init__(self, prop, value, targets = None, op = Operator.Update):

        self.__targets = targets
        self.__prop = prop
        self.__op = op
        self.__opVal = value
        self.__targetObj = None
        self.__targetAttr = None

    def parse_target_attr(self):
        if not self.__targets:
            assert self.__prop.startswith('@')

    def get_target_property(self):
        return self.__target

    def get_result(self, originVal, opVal):
        if self.__op == Operator.Update:
            return opVal
        elif self.__op == Operator.Add:
            return originVal + opVal
        elif self.__operator == Operator.Subtract:
            return originVal - opVal
        elif self.__operator == Operator.Multiply:
            return originVal * opVal
        else:
            return originVal

    def get_rt_value(self, scene):
        return self.__opVal.gen_runtime_obj(scene)


    def gen_runtime_obj(self, scene):

        def updates():
            val_func = self.get_rt_value(scene)
            if not val_func:
                return None
            val = val_func()

            if type(self.__prop) is VarRef:
                var = self.__prop.gen_runtime_obj(scene)()
                if var:
                    fininal_val = self.get_result(var.get_value(), val.get_value())
                    var.set_value(fininal_val)
            elif type(self.__prop) is AttrName and self.__targets:
                targets = []
                func1 = self.__targets.gen_runtime_obj(scene)
                if func1:
                    targets = func1()
                for t in targets:
                    o_val = t.get_prop_value(self.__prop.get_name())
                    if o_val :
                        f_val = self.get_result(o_val, val)
                        t.upate_prop(self.__prop.get_name(), f_val)

        return updates


