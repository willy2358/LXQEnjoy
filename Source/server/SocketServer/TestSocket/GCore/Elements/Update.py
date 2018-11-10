
from GCore.Operator import Operator
from GCore.Statement import Statement
from GCore.Engine import *
import GCore.Engine

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

    def get_result(self, originVal):
        if self.__op == Operator.Update:
            return self.__opVal
        elif self.__op == Operator.Add:
            return originVal + self.__opVal
        elif self.__operator == Operator.Subtract:
            return originVal - self.__opVal
        elif self.__operator == Operator.Multiply:
            return originVal * self.__opVal
        else:
            return originVal

    # def parse_attr_statement(self, attrValue):
    #     pass

    # def get_final_target_objects(self, scene):
    #     objs = []
    #     if not self.__targets:
    #         if self.__prop.startswith("@round."):
    #             r = scene.get_current_round()
    #             attr = r.get_attr(self.__prop)
    #             objs.append(attr)
    #         elif self.__prop.startswith("@scene."):
    #             objs.append( scene.get_attr(self.__prop))
    #         elif self.__prop.startswith("@"):
    #             objs.append(scene.get_var(self.__prop))
    #
    #     else:
    #         pass
    #
    #     return objs

    def get_rt_target_objs(self, scene):
        objs = []
        if self.__prop.startswith("@round."):
            r = scene.get_current_round()
            attr = r.get_attr(self.__prop.lstrip("@round"))
            objs.append(attr)
        elif self.__prop.startswith("@scene."):
                objs.append( scene.get_attr(self.__prop.lstrip("@scene")))
        elif self.__prop.startswith("@"):
                objs.append(scene.get_var(self.__prop.lstrip("@")))
        elif len(self.__prop) > 0 and self.__targets:
            insts = self.__targets.gen_runtime_obj(scene)
            if insts:
                for inst in insts:
                    obj = inst.get_prop_value(self.__prop)
                    if obj:
                        objs.append(obj)

        return objs

    def get_rt_value(self, scene):
        return self.__opVal.get_runtime_obj(scene)


    def gen_runtime_obj(self, scene):
        def updates():
            target_objs = self.get_rt_target_objs(scene)
            if not target_objs:
                return
            val_func = self.get_rt_value(scene)
            val = val_func()
            fininal_val = self.get_result(val)
            for obj in target_objs:
                obj.set_value(fininal_val)
        return updates


