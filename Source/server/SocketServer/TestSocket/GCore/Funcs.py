
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

def cards_count_not_deal(scene, args):
    rund = scene.get_current_round()
    return rund.undealing_cards_count()


def element_at(scene, args):
    try:
        arr, idx = args[0], int(args[1])
        if isinstance(arr, list):
            if 0 <= idx < len(arr):
                return arr[idx]
    except Exception as ex:
        Log.exception(ex)
        return  None

# count_of(scene, list)
def count_of(scene, args):
    try:
        lsObj = args[0]
        return len(lsObj)
    except Exception as ex:
        Log.exception(ex)
        return 0


#next_player_of(scene, player, dis=1)
def next_player_of(scene, args):
    player = args[0]
    dis = 1
    if len(args) > 1:
        dis = int(args[1])
    return scene.get_next_player(player)


#player_has_cards(scene, player, cards)
def player_has_cards(scene, args):
    try:
        player = args[0]
        cards = args[1]
        return player.has_cards(cards)
    except Exception as ex:
        Log.exception(ex)
        return False

def player_cards_of_free(scene, args):
    pass

def player_cards_of_shown(scene, args):
    pass

def player_cards_of_frozen(scene, args):
    pass



def to_list(scene, args):
    return args

__maps = {'ctype_of' : ctype_of,
          'cfigure_of': cfigure_of,
          'cards_count_not_deal': cards_count_not_deal,
          'count_of':count_of,
          'element_at':element_at,
          'next_player_of':next_player_of,
          'player_has_cards':player_has_cards,
          'to_list':to_list,
          }


def invoke(func_name, scene, args):
    try:
        if func_name in __maps:
            return __maps[func_name](scene, args)
        elif func_name.startswith("#"):
            return scene.call_proc(func_name.lstrip('#'), args)
        else:
            Log.error("Not existing func name:" + func_name)
    except Exception as ex:
        Log.exception(ex)


