from GCore.Statement import Statement
import Mains.Log as Log
# <action name="koupai" text="koupai">
#             <send_cards_to_table cards="@selected_cards"/>
#             <delay seconds="2"/>
#             <pub_msg players="@round.players" msg="kou pai"></pub_msg>
# </action>
# < !--对于action，其内部可访问两个隐含的参数：
# @cmd_player: 执行此action的player
#
# @cmd_args :执行action传入的参数
# -->
class Action(Statement):
    def __init__(self, name):
        super(Action, self).__init__()
        self.__name = name
        self.__statements = []
        self.__check_param = None

    def get_name(self):
        return self.__name

    def add_statement(self, stm):
        self.__statements.append(stm)

    def set_check_param_statement(self, stm):
        self.__check_param = stm

    def gen_param_check_func(self, scene):
        if not self.__check_param:
            return None
        return self.__check_param.gen_runtime_obj(scene)

    def gen_runtime_obj(self, scene):
        def act_func():
            Log.debug("Executing:{0} ....".format(self.get_step()))
            try:
                rtObjs = []
                for c in self.__statements:
                    func = c.gen_runtime_obj(scene)
                    if callable(func):
                        func()
            except Exception as ex:
                Log.exception(ex)
        return act_func



