from GCore.Statement import Statement

class ProcRef(Statement):
    def __init__(self, procName):
        super(ProcRef, self).__init__()
        self.__proc_name = procName