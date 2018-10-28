
from GRules.RulePart_Actions import RulePart_Actions
from GRules.RulePart_Cards import RulePart_Cards
from GRules.RulePart_Following import RulePart_Following
from GRules.RulePart_Players import RulePart_Players
from GRules.RulePart_Round import RulePart_Round
from GRules.RulePart_Running import RulePart_Running
from GRules.RulePart_Trick import RulePart_Trick
from GRules.RulePart_Procs import RulePart_Procs
from GRules.RulePart_Scene import RulePart_Scene

def create_part(partName, xmlNode, gRule):
    if partName == RulePart_Cards.PART_NAME:
        return RulePart_Cards(xmlNode, gRule)
    elif partName == RulePart_Following.PART_NAME:
        return RulePart_Following(xmlNode, gRule)
    elif partName == RulePart_Players.PART_NAME:
        return RulePart_Players(xmlNode, gRule)
    elif partName == RulePart_Procs.PART_NAME:
        return RulePart_Procs(xmlNode, gRule)
    elif partName == RulePart_Trick.PART_NAME:
        return RulePart_Trick(xmlNode, gRule)
    elif partName == RulePart_Scene.PART_NAME:
        return RulePart_Scene(xmlNode, gRule)
    elif partName == RulePart_Round.PART_NAME:
        return RulePart_Round(xmlNode, gRule)
    elif partName == RulePart_Running.PART_NAME:
        return RulePart_Running(xmlNode, gRule)
    elif partName == RulePart_Actions.PART_NAME:
        return RulePart_Actions(xmlNode, gRule)

    else:
        return None