
from Patterns.Pattern_Single import Pattern_Single
from Patterns.Pattern_Comp import Pattern_Comp
from Patterns.Pattern_QGroup import Pattern_QGroup
from Patterns.Pattern_Seqm import Pattern_Seqm
from Patterns.Pattern_Seq import Pattern_Seq
from Patterns.Pattern_SameCfigure import Pattern_SameCfigure
from Patterns.Pattern_SameCtype import Pattern_SameCtype

def create_pattern(elemName, xmlElement):
    pat = None
    if elemName == Pattern_Single.ELEMENT_NAME:
        pat = Pattern_Single()
    elif elemName == Pattern_SameCfigure.ELEMENT_NAME \
            or elemName == Pattern_SameCfigure.ELEMENT_PAIR\
            or elemName == Pattern_SameCfigure.ELEMENT_TRIPLE\
            or elemName == Pattern_SameCfigure.ELEMENT_QUAD:
        pat = Pattern_SameCfigure()
    elif elemName == Pattern_Seq.ELEMENT_NAME:
        pat = Pattern_Seq()
    elif elemName == Pattern_Seqm.ELEMENT_NAME:
        pat = Pattern_Seqm()
    elif elemName == Pattern_Comp.ELEMENT_NAME:
        pat = Pattern_Comp()
    elif elemName == Pattern_QGroup.ELEMENT_NAME:
        pat = Pattern_QGroup()
    elif elemName == Pattern_SameCtype.ELEMENT_NAME:
        pat = Pattern_SameCtype()

    if pat is not None and pat.load(xmlElement):
        return pat

