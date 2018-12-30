from GCore.ValueType import ValueType
from GCore.CValue import CValue
import Mains.Log as Log

class GVar:
    def __init__(self, name, vType = ValueType.integer, val = None):
        self.__name = name
        self.__vType = vType
        self.__value = val
        if not val or (isinstance(val, CValue) and not val.get_value()):
            if vType == ValueType.players or vType == ValueType.cards:
                self.__value = []
        self._is_pub_status = False


    def get_name(self):
        return self.__name

    def get_value(self):
        return self.__value

    def get_value_type(self):
        return self.__vType

    def get_value_type_name(self):
        return ValueType.get_type_str(self.__vType)

    def is_pub_status(self):
        return self._is_pub_status

    def set_is_pub_status(self):
        self._is_pub_status = True

    def set_value(self, val):
        from Mains.Player import Player
        valR = val
        if isinstance(valR, CValue):
            valR = valR.get_value()
        elif isinstance(valR, Player):
            valR = " player of id:{0}".format(valR.get_userid())

        Log.debug("Update var {0} from {1} to {2}".format(self.__name, self.__value, valR))
        self.__value = val

