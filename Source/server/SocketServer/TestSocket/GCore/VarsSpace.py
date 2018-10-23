
__Vars = {} #xmlNode: {'var_name':value}


def update(xmlNode, var_name, var_val):
    if xmlNode not in __Vars:
        __Vars[xmlNode] = {}

    __Vars[xmlNode][var_name] = var_val
