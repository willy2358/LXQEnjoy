from GCore.Statement import Statement

#sleep for some seconds
class Delay(Statement):
    def __init__(self, seconds):
        super(Delay, self).__init__()
        self.__seconds = seconds
