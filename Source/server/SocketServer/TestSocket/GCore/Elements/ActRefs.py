from GCore.Statement import Statement

#<act_refs acts="@act"/>
class ActRefs(Statement):
    def __init__(self, acts):
        self.__acts = acts