
from Mains.GVar import GVar
from GCore.ValueType import ValueType

from GCore.VarRef import VarRef


class ExtAttrs:
    def __init__(self):
        self.__cus_attrs = {}  # name:GVar
        self.__vars = {}  # name:GVar

    def get_attr_value(self, attrName):
        if attrName in self.__cus_attrs:
            val = self.__cus_attrs[attrName].get_value()
            if type(val) is VarRef :
                obj = val.gen_runtime_obj(self)()
                if type(obj) is GVar:
                    return obj.get_value()
                else:
                    return obj
            return val
        else:
            return None

    def get_var_value(self, varName):
        if varName in self.__vars:
            val = self.__vars[varName].get_value()
            if type(val) is VarRef:
                obj = val.gen_runtime_obj(self)()
                if type(obj) is GVar:
                    return obj.get_value()
                else:
                    return obj
            return val
        else:
            return None

    def get_prop_value(self, propName):
        if propName in self.__cus_attrs:
            return self.get_attr_value(propName)
        elif propName in self.__vars:
            return self.get_var_value(propName)
        else:
            return None


    def get_var(self, varName):
        if varName in self.__vars:
            return self.__vars[varName]
        else:
            return None

    def get_attr(self, attrName):
        if attrName in self.__cus_attrs:
            return self.__cus_attrs[attrName]
        else:
            return None

    def get_prop(self, propName):
        if propName in self.__cus_attrs:
            return self.__cus_attrs[propName]
        elif propName in self.__vars:
            return self.__vars[propName]
        else:
            return None

    def get_attrs(self):
        return self.__cus_attrs

    def get_vars(self):
        return self.__vars

    def add_cus_attr(self, attrName, attrType = 'integer', attrVal=None):
        self.__cus_attrs[attrName] = GVar(attrName, attrType, attrVal)

    def update_attr(self, attrName, value):
        if attrName in self.__cus_attrs:
            self.__cus_attrs[attrName].set_value(value)


    def add_variable(self, name, vtype, value):
        if name not in self.__vars:
            self.__vars[name] = GVar(name, ValueType.undef, value)

    def update_variable(self, name, value):
        if name not in self.__vars:
            self.__vars[name] = GVar(name, ValueType.undef, value)
        else:
            self.__vars[name].set_value(value)

    def upate_prop(self, propName, value):
        if propName in self.__cus_attrs:
            self.__cus_attrs[propName] = value
        elif propName in self.__vars:
            self.__vars[propName] = value



