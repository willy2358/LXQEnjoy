
from GRules.RulePart_Actions import RulePart_Actions
from GRules.RulePart_Cards import RulePart_Cards
from GRules.RulePart_Following import RulePart_Following
from GRules.RulePart_Players import RulePart_Players
from GRules.RulePart_Round import RulePart_Round
from GRules.RulePart_Running import RulePart_Running
from GRules.RulePart_Trick import RulePart_Trick

def create_part(partName, xmlNode):
    if partName == "cards":
        return RulePart_Cards(xmlNode)
    elif partName == "following":
        return RulePart_Following(xmlNode)
    elif partName == "players":
        return RulePart_Players(xmlNode)
    elif partName == "trick":
        return RulePart_Trick(xmlNode)
    elif partName == "round":
        return RulePart_Round(xmlNode)
    elif partName == "running":
        return RulePart_Running(xmlNode)
    elif partName == "actions":
        return RulePart_Actions(xmlNode)
    else:
        return None