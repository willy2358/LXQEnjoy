from GCore.Statement import Statement



# <update_player player="@p1">
#     <update property="IsMainPlayer" value="false"/>
# </update_player>
# <update_player property="seatid" value="@seatid + 1">
#     <update property="IsMainPlayer" value="true"/>
# </update_player>
class UpdatePlayer(Statement):
    def __init__(self):
        self.__test_prop = None
        self.__test_value = ""
        self.__from_var = None
        self.__updates = []

    def set_from_var(self, var_name):
        self.__from_var = var_name

    def set_test_property(self, propName, value):
        self.__test_prop = propName
        self.__test_value = value

    def add_update(self, statement):
        self.__updates.append(statement)

    def gen_runtime_obj(self, scene):
        def update_player():
            acep = None
            players = scene.get_players()
            if self.__test_prop and self.__test_value:
                for p in players:
                    if p.is_attr_meet(self.__test_prop, self.__test_value):
                        acep = p
                        break
            elif self.__from_var:
                acep = scene.get_var_value(self.__from_var)
            if acep:
                for upd in self.__updates:
                    propName = upd.get_target_property()
                    oriVal = acep.get_attr_value(propName)
                    if not oriVal:
                        continue
                    retVal = upd.get_result(oriVal)
                    acep.update_attr(propName, retVal)

        return update_player


