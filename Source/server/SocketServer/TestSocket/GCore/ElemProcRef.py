from GCore.Statement import Statement

class ProcRef(Statement):
    def __init__(self, procName):
        self.__proc_name = procName