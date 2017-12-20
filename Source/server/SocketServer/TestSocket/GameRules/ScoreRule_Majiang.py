

# B short for base score
# P short for pattern score
# W short for zimo score
# N short for ting kou score
# G short for cards group score
class ScoreRule_Majiang:
    def __init__(self):
        self.__base_score = 0  # short for B in score formular
        self.__pattern_score = {} # short for P in score formular
        self.__none_pattern_score = 1 # the min score
        self.__zimo_score = 2  # short for W in score formular

        # if the number of ting-kou is different, its score are different too
        # for example, only one kou, having the most score, if number of kou is 2, its score is less
        # short for N in score formular
        self.__ting_kou_score = {}

        # in some playing type, some cards group also count, for example, gang(4 same figures), peng(3 same figures)
        # short for G in score formular
        self.__cards_group_score = {}

        self.__score_formular = ""

    def get_base_score(self):
        return self.__base_score

    def get_pattern_score(self, pattern_name):
        if pattern_name in self.__pattern_score:
            return self.__pattern_score[pattern_name]
        else:
            return self.__none_pattern_score

    def get_zimo_score(self):
        return self.__zimo_score

    def get_ting_kou_score(self, kou_num):
        if kou_num in self.__ting_kou_score:
            return self.__ting_kou_score[kou_num]
        else:
            key = max(self.__ting_kou_score.keys())
            return self.__ting_kou_score[key]

    def get_group_score(self, group):
        if group in self.__cards_group_score:
            return self.__cards_group_score[group]
        else:
            return 0

    def get_scored_groups(self):
        return self.__cards_group_score

    def is_calculate_ting_kou_num(self):
        return len(self.__ting_kou_score) > 0

    def is_calculate_cards_group(self):
        return len(self.__cards_group_score) > 0


    def set_pattern_score(self, pattern_name, score):
        self.__pattern_score[pattern_name] = score

    def set_base_score(self, score):
        self.__base_score = score

    def set_score_formular(self, formular):
        self.__score_formular = formular

    def set_zimo_score(self, score):
        self.__zimo_score = score

    def set_ting_kou_count_score(self, kou_num, score):
        self.__ting_kou_score[kou_num] = score

    def set_cards_group_score(self, group, score):
        self.__cards_group_score[group] = score


    def calculate_score(self, B=1,G=0, N=1,P=1,W=1):
        expr = self.__score_formular
        expr = expr.replace('B',str(B)).replace('P',str(P)).replace('W',str(W)).replace('N',str(N)).replace('G',str(G))
        try:
            score = eval(expr)
            return score
        except Exception as e:
            print(e)