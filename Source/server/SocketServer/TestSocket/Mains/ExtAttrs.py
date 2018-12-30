
from Mains.GVar import GVar
from GCore.ValueType import ValueType
from GCore.CValue import CValue

from GCore.VarRef import VarRef
import Mains.Log as Log


class ExtAttrs:
    def __init__(self):
        self.__cus_attrs = {}  # name:GVar
        self.__vars = {}  # name:GVar

    def get_attr_value(self, attrName):
        Log.debug('get_attr_value:{0},...'.format(attrName))
        finalVal = None
        if attrName in self.__cus_attrs:
            val = self.__cus_attrs[attrName].get_value()
            if type(val) is VarRef :
                obj = val.gen_runtime_obj(self)()
                if type(obj) is GVar:
                    finalVal = obj.get_value()
                else:
                    finalVal = obj
            else:
                finalVal = val
        Log.debug('got attr value {0}'.format(finalVal))
        return finalVal

    def get_var_value(self, varName):
        Log.debug('get_var_value:{0},...'.format(varName))
        finalVal = None
        if varName in self.__vars:
            val = self.__vars[varName].get_value()
            if type(val) is VarRef:
                obj = val.gen_runtime_obj(self)()
                if type(obj) is GVar:
                    # return obj.get_value()
                    finalVal = obj.get_value()
                else:
                    # return obj
                    finalVal = obj
            # return val
            finalVal = val
        # else:
        #     return None
        Log.debug('got var value {0}'.format(finalVal))
        return finalVal

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

    def get_pub_attrs(self):
        attrs = []
        for attr in self.__cus_attrs:
            varObj = self.__cus_attrs[attr]
            if varObj.is_pub_status():
                attrs.append(varObj)

        return attrs

    def get_attrs(self):
        return self.__cus_attrs

    def get_vars(self):
        return self.__vars

    def add_cus_attr(self, attrName, attrType = 'integer', attrVal=None, is_pub_status=False):
        gVar = GVar(attrName, attrType, attrVal)
        if is_pub_status:
            gVar.set_is_pub_status()
        self.__cus_attrs[attrName] = gVar


    def update_attr(self, attrName, value):
        if attrName in self.__cus_attrs:
            self.__cus_attrs[attrName].set_value(value)


    def add_variable(self, name, vtype, value, scope=None):
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



