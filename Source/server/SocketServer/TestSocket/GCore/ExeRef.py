from GCore.Statement import Statement

# <exeref ref="@trick.end"/>
class ExeRef(Statement):
    def __init__(self, ref):
        self.__refered_proc = ref