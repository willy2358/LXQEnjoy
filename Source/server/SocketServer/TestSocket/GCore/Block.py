
from GCore.Operation import Operation

class Block(Operation):
    def __init__(self):
        self.__operations = []


    def add_operation(self, operation):
        self.__operations.append(operation)
