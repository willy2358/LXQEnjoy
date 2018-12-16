
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
# <update property="@round.winners.[].IsDefender" value="true"/>
# <update property="@players.[].Score" value="20"/>
class Update(Statement):
    def __init__(self, prop, value, op = Operator.Update):
        super(Update, self).__init__()
        self.__prop = prop
        self.__op = op
        self.__opVal = value
        # self.__targetObj = None
        # self.__targetAttr = None

    # def parse_target_attr(self):
    #     if not self.__targets:
    #         assert self.__prop.startswith('@')

    # def get_target_property(self):
    #     return self.__target

    def get_result(self, scene, originVal, opVal):
        rawVal = originVal
        if type(originVal) is GVar:
            rawVal = scene.get_prop_value(originVal.get_name())
        if type(rawVal) is CValue:
            rawVal = rawVal.get_value()

        if self.__op == Operator.Update:
            return opVal

        if isinstance(originVal, list):
            newObjs = originVal[:]
            if self.__op == Operator.Append:
                if isinstance(opVal, list):
                    return newObjs + opVal
                else:
                    # todo : following can be optimized to  originVal.append(opVal)
                    newObjs.append(opVal)
                    return newObjs
            elif self.__op == Operator.Remove:
                if isinstance(opVal, list):
                    Utils.list_remove_parts(newObjs, opVal)
                    return newObjs
                elif opVal in newObjs:
                    newObjs.remove(opVal)
                    return newObjs
            else:
                Log.error("Invalid op for list:" + self.__op)
                return newObjs


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
                Log.debug("Executing update :{0} ....".format(self.get_step()))
                opVal = scene.get_obj_value(self.__opVal)
                # if opVal:
                #     Log.error("Value attr should not none at var :{0}".format(self.__opVal))
                if isinstance(self.__prop, VarRef):
                    objs = []
                    rtVar = scene.get_rt_var(self.__prop)
                    if not rtVar:
                        Log.error("Prop attr should not none at var :{0}".format(self.__prop))

                    if isinstance(rtVar, list):
                        objs = rtVar[:]
                    elif rtVar:
                        objs.append(rtVar)
                    for obj in objs:
                        oriVal = scene.get_obj_value(obj)
                        fininal_val = self.get_result(scene, oriVal, opVal)
                        obj.set_value(fininal_val)

            except Exception as ex:
                Log.exception(ex)

        return updates


