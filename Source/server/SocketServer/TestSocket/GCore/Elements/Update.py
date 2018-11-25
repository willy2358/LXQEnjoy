
from GCore.Operator import Operator
from GCore.Statement import Statement
from GCore.Engine import *
import GCore.Engine
from GCore.VarRef import VarRef
from Mains.GVar import GVar
from GCore.CValue import CValue
import Mains.Log as Log

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

    def get_result(self, scene, originVal, opVal):
        rawVal = originVal
        if type(originVal) is GVar:
            rawVal = scene.get_prop_value(originVal.get_name())
        if type(rawVal) is CValue:
            rawVal = rawVal.get_value()

        if self.__op == Operator.Update:
            return opVal
        if not str(rawVal).isnumeric():
            return rawVal

        if self.__op == Operator.Add:
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
            try:
                opVal = scene.get_obj_value(self.__opVal)

                if isinstance(self.__prop, VarRef):
                    objs = []
                    rtVar = scene.get_rt_var(self.__prop)
                    if isinstance(rtVar, list):
                        objs = rtVar[:]
                    elif rtVar:
                        objs.append(rtVar)
                    for obj in objs:
                        oriVal = scene.get_obj_value(obj)
                        fininal_val = self.get_result(scene, oriVal, opVal)
                        obj.set_value(fininal_val)
                elif type(self.__prop) is AttrName and self.__targets:
                    targets = scene.get_obj_value(self.__targets)
                    for t in targets:
                        o_val = t.get_prop(self.__prop.get_name())
                        if o_val :
                            f_val = self.get_result(o_val.get_value(), opVal)
                            # o_val is a GVar
                            o_val.set_value(f_val)
            except Exception as ex:
                Log.exception(ex)

        return updates


