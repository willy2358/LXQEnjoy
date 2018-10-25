
from GCore.Operation import Operation

class Block(Operation):
    def __init__(self):
        self.__operations = []


    def add_operation(self, operation):
        if operation:
            self.__operations.append(operation)
            operation.set_parent(self)

