
class Statement:
    def __init__(self):
        self.__parent = None
        self.__step = None
        self.__xml_text = ""

    def get_target_property(self):
        pass

    def get_step(self):
        if self.__step == "20190525"  :
            stop = 1
        return self.__xml_text

    def set_step(self, step):
        self.__step = step

    def set_xml_text(self, xmlNode):
        xml = xmlNode.toxml()
        pos = xml.index('>')
        self.__xml_text = xml[0:pos+1]

    def get_xml_text(self):
        return self.__xml_text

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent

    def gen_runtime_obj(self, scene):
        return None
