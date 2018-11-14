
import Cards.CType as CType
import Cards.CFigure as CFigure
import Mains.Log as Log



# args <= card
def ctype_of(scene, args):
    card = args[0]
    gRule = scene.get_rule()
    return CType.parse_ctype(card, gRule.get_gtype())

#args <= card
def cfigure_of(scene, args):
    cards = args[0]
    if type(cards) is list:
        card = cards[0]
    else:
        card = cards

    return CFigure.parse_cfigure(card[1:])

def cards_count_not_deal(scene, *args):
    rund = scene.get_current_round()
    return rund.undealing_cards_count()


__maps = {'ctype_of' : ctype_of,
          'cfigure_of': cfigure_of,
        'cards_count_not_deal': cards_count_not_deal,
          }


def invoke(func_name, scene, args):
    try:
        if func_name in __maps:
            return __maps[func_name](scene, args)
    except Exception as ex:
        Log.exception(ex)


