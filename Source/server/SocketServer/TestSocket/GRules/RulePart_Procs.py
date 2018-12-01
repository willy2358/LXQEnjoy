from GRules.RulePart import RulePart
import GCore.Engine
import Utils

class RulePart_Procs(RulePart):
    PART_NAME = "procs"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Procs, self).__init__(xmlNode, gRule)
        self.__procs = []

    def parse(self):
        xmlNode = self.get_xml_node()
        if not xmlNode:
            return False

        try:
            for elem in Utils.getXmlChildElments(xmlNode):
                proc = GCore.Engine.parse_elem_proc(elem, self.getGRule())
                if proc:
                    self.__procs.append(proc)

            return True
        except Exception as ex:
            raise ex

    def get_procs(self):
        return self.__procs

    def add_proc(self, procStm):
        self.__procs.append(procStm)

    def get_part_name(self):
        return self.PART_NAME