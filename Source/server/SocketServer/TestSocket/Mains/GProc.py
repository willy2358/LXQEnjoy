
class GProc:
    def __init__(self):
        self.__params = {}
        self.__statements = []
        self.__exec_func = None
    def set_param(self, paramName, paramValue):
        self.__params[paramName] = paramValue

    def set_exec_func(self, func):
        self.__exec_func = func

    def exec_func(self):
        pass
