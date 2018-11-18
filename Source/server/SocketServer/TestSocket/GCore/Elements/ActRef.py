
from Mains.PlayCmd import PlayCmd
from GCore.Statement import Statement
# from Mains.PlayScene import PlayScene

#<act_ref act="jiaozhu" param="@drawn_card"/>
class ActRef(Statement):
    def __init__(self, act_ref, param):
        self.__ref_act_name = act_ref
        self.__param = param

    def get_act_name(self):
        return self.__ref_act_name

    def gen_runtime_obj(self, scene):
        def ret_cmd():
            cmd = PlayCmd(None, self.__ref_act_name, scene.get_obj_value(self.__param))
            return cmd
        return ret_cmd




