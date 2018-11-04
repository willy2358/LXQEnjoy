from GCore.Statement import Statement

# <action name="koupai" text="koupai">
#             <send_cards_to_table cards="@selected_cards"/>
#             <delay seconds="2"/>
#             <pub_msg players="@round.players" msg="kou pai"></pub_msg>
#         </action>
class Action(Statement):
    def __init__(self, name):
        self.__name = name
        self.__statements = []

    def add_statement(self, stm):
        self.__statements.append(stm)

    def gen_runtime_obj(self, scene):
        pass



