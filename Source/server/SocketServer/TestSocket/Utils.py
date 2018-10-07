from xml.dom.minidom import parse
import xml.dom.minidom

def list_remove_parts(src_list, parts):
    for i in parts:
        if i in src_list:
            src_list.remove(i)

    return src_list


def getFirstNamedChild(tagName, parentNode):
    if not parentNode or not tagName:
        return None

    for child in parentNode.childNodes:
        if type(child) is not xml.dom.minidom.Element:
            continue
        if child.tagName == tagName:
            return child

    return None