
from Mains.GVar import GVar
from GCore.ValueType import ValueType
from GCore.Operator import Operator

class ExtAttrs:
    def __init__(self):
        self.__cus_attrs = {}  # name:GVar
        self.__vars = {}  # name:GVar

    def get_attr_value(self, attrName):
        if attrName in self.__cus_attrs:
            return self.__cus_attrs[attrName].get_value()
        else:
            return None

    def get_var_value(self, varName):
        if varName in self.__vars:
            return self.__vars[varName].get_value()
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

    def get_prop_value(self, propName):
        if propName in self.__cus_attrs:
            return self.__cus_attrs[propName]
        elif propName in self.__vars:
            return self.__vars[propName]
        else:
            return None

    def is_meet_conditions(self, named_attrs, op):
        # no requirements, return false
        if not named_attrs:
            return False

        if op == Operator.Or:
            for k, v in named_attrs:
                if v == self.get_prop_value(k):
                    return True
            return False
        if op == Operator.And:
            for k, v in named_attrs:
                if v != self.get_prop_value(k):
                    return False
            return True
        return False

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

