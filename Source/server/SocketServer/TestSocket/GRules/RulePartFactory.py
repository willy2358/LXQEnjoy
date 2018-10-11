
from GRules.RulePart_Actions import RulePart_Actions
from GRules.RulePart_Cards import RulePart_Cards
from GRules.RulePart_Following import RulePart_Following
from GRules.RulePart_Players import RulePart_Players
from GRules.RulePart_Round import RulePart_Round
from GRules.RulePart_Running import RulePart_Running
from GRules.RulePart_Trick import RulePart_Trick

def create_part(partName, xmlNode, gRule):
    if partName == "cards":
        return RulePart_Cards(xmlNode, gRule)
    elif partName == "following":
        return RulePart_Following(xmlNode, gRule)
    elif partName == "players":
        return RulePart_Players(xmlNode, gRule)
    elif partName == "trick":
        return RulePart_Trick(xmlNode, gRule)
    elif partName == "round":
        return RulePart_Round(xmlNode, gRule)
    elif partName == "running":
        return RulePart_Running(xmlNode, gRule)
    elif partName == "actions":
        return RulePart_Actions(xmlNode, gRule)
    else:
        return None