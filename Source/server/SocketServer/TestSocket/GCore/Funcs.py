
import Cards.CType as CType
import Cards.CFigure as CFigure

# args <= card
def ctype_of(scene, *args):
    card = args[0]
    gRule = scene.get_rule()
    return CType.parse_ctype(card, gRule.get_gtype())

#args <= card
def cfigure_of(scene, *args):
    card = args[0]
    return CFigure.parse_cfigure(card[1:])


__maps = {'ctype_of' : ctype_of,
          'cfigure_of': cfigure_of,

          }


def invoke(func_name, scene, *args):
    if func_name in __maps:
        return __maps[func_name](scene, args)
