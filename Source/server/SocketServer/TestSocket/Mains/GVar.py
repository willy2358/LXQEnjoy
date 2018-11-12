from GCore.ValueType import ValueType

class GVar:
    def __init__(self, name, vType = ValueType.integer, val = None):
        self.__name = name
        self.__vType = vType
        self.__value = val

    def get_name(self):
        return self.__name

    def get_value(self):
        return self.__value

    def get_value_type(self):
        return self.__vType

    def set_value(self, val):
        self.__value = val

