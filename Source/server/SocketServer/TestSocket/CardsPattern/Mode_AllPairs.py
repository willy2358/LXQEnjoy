from CardsPattern.Mode import Mode

class Mode_AllPairs(Mode):
    """description of class"""
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)


    def is_match(self, faces):
        uniq = set(faces)
        return len(faces)%2 == 0 and len(uniq) == len(faces)/2