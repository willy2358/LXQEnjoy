
import Cards.CType as CType
import Cards.CFigure as CFigure
import Mains.Log as Log

# args: none
def cards_count_not_deal(scene, args):
    rund = scene.get_current_round()
    return rund.undealing_cards_count()

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


# count_of(scene, list)
def count_of(scene, args):
    try:
        lsObj = args[0]
        return len(lsObj)
    except Exception as ex:
        Log.exception(ex)
        return 0

def ctype_count_of_cards(scene, args):
    pass

def cfigure_count_of_cards(scene, args):
    pass

def cards_contain_same_figure(scene, args):
    pass


def element_at(scene, args):
    try:
        arr, idx = args[0], int(args[1])
        if isinstance(arr, list):
            if 0 <= idx < len(arr):
                return arr[idx]
    except Exception as ex:
        Log.exception(ex)
        return  None

def find_player(scene, args):
    pass

def find_players(scene, args):
    pass


#args: cards, pattern(single,pair,triple,quad,same_type,
#def is_cards_match_pattern(scene, args):
def is_cards_same_ctype(scene, args):
    pass

def is_cards_same_cfigure(scene, args):
    pass

# args: cards, ctype
def is_cards_contain_ctype(scene, args):
    pass

# args: cards, cfigure
def is_cards_contain_cfigure(scene, args):
    pass

# args: player, ctype
def is_player_has_cards_of_ctype(scene, args):
    pass

# args: player, cfigure
def is_player_has_cards_of_cfigure(scene, args):
    pass


# args: cards
def max_cfigure_of_cards(scene, args):
    pass

# args: attrName
def max_attr_of_player(scene, args):
    pass

# args: cards
def min_cfigure_of_cards(scene, args):
    pass

#next_player_of(scene, player, dis=1)
def next_player_of(scene, args):
    player = args[0]
    dis = 1
    if len(args) > 1:
        dis = int(args[1])
    return scene.get_next_player(player)

# args: cards, cfigure
def parts_of_cards_of_cfigure(scene, args):
    pass

# args: cards, cfigure
def parts_of_cards_ex_cfigure(scene, args):
    pass

# args: cards, ctype
def parts_of_cards_of_ctype(scene, args):
    pass

# args: cards, ctype
def parts_of_cards_ex_ctype(scene, args):
    pass

#player_has_cards(scene, player, cards)
def player_has_cards(scene, args):
    try:
        player = args[0]
        cards = args[1]
        return player.has_cards(cards)
    except Exception as ex:
        Log.exception(ex)
        return False

#args: player
def player_cards_of_free(scene, args):
    pass

def player_cards_of_shown(scene, args):
    pass

def player_cards_of_frozen(scene, args):
    pass

# args: player, cfigure
def player_cards_of_cfigure(scene, args):
    pass

# args: player, ctype
def player_cards_of_ctype(scene, args):
    pass

def sum_cards_cfigure(scene, args):
    pass

def to_list(scene, args):
    return args

__maps = {
            'cards_count_not_deal': cards_count_not_deal,
            'cards_contain_same_figure':cards_contain_same_figure,
            'cfigure_of': cfigure_of,
            'cfigure_count_of_cards': cfigure_count_of_cards,

            'count_of': count_of,
            'ctype_of' : ctype_of,
            'ctype_count_of_cards':ctype_count_of_cards,

            'element_at':element_at,
            'is_cards_contain_ctype':is_cards_contain_ctype,
            'is_cards_contain_cfigure':is_cards_contain_cfigure,
            'is_cards_same_ctype':is_cards_same_ctype,
            'is_cards_same_cfigure':is_cards_same_cfigure,

            'is_player_has_cards_of_ctype':is_player_has_cards_of_ctype,
            'is_player_has_cards_of_cfigure':is_player_has_cards_of_cfigure,
            'next_player_of':next_player_of,
            'parts_of_cards_of_cfigure':parts_of_cards_of_cfigure,
            'parts_of_cards_ex_cfigure':parts_of_cards_ex_cfigure,
            'parts_of_cards_of_ctype':parts_of_cards_of_ctype,
            'parts_of_cards_ex_ctype': parts_of_cards_ex_ctype,
            'player_cards_of_free':player_cards_of_free,
            'player_cards_of_shown':player_cards_of_shown,
            'player_cards_of_frozen':player_cards_of_frozen,
            'player_cards_of_ctype':player_cards_of_ctype,
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


