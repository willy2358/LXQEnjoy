

class ScoresRule_Majiang:
    def __init__(self):
        self.__base_score = 0
        self.__patttern_score = {}
        self.__is_zimo = False
        self.__num_ting_kou = 1
        self.__cards_group = 1
        self.__score_formular = ""

    def get_base_score(self):
        return self.__base_score

    def get_pattern_score(self, pattern_name):
        return self.__patttern_score[pattern_name]

    def set_pattern_score(self, pattern_name, score):
        self.__patttern_score[pattern_name] = score

    def set_base_score(self, score):
        self.__base_score = score

    def set_score_formular(self, formular):
        self.__score_formular = formular

    def calculate_score(self):
        return 0
