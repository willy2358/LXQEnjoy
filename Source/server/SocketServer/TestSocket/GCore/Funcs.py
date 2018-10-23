
def ctype_of(card):
    pass

def cfigure_of(card):
    pass


__maps = {'ctype_of' : ctype_of,
          'cfigure_of': cfigure_of,

          }

def invoke(func_name, *args):
    if func_name in __maps:
        __maps[func_name](args)
