from GCore.Operand import Operand
from GCore.ValueType import ValueType
import Mains.Log as Log

class Variable(Operand):
    def __init__(self, varName):
        super(Variable, self).__init__(None)
        self.__name = varName
        self.__value_type = ValueType.undef
        self.__value = None
        self.__is_pub_status = False

    def get_name(self):
        return self.__name

    def get_value_type(self):
        return self.__value_type

    def get_value(self):
        return self.__value

    def get_value(self):
        return self.__value

    def is_pub_status(self):
        return self.__is_pub_status

    def set_value_type(self, vtype):
        self.__value_type = vtype

    def set_value(self, val):
        self.__value = val

    def set_pub_status(self):
        self.__is_pub_status = True

    def gen_runtime_obj(self, scene):
        def new_var(scope=None):
            try:
                Log.debug("executing:{1} ....".format(self.get_name(), self.get_step()))
                name = self.get_name()
                vtype = self.get_value_type()
                val = self.get_value()
                val = scene.get_obj_value(val)
                if name.startswith("#"):
                    scene.add_proc_local_var(name, vtype, val, scope)
                else:
                    scene.add_variable(name, vtype, val, scope)
            except Exception as ex:
                Log.exception(ex)
        return new_var



