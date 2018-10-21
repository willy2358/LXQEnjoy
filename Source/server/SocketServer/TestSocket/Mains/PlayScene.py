
from GRules.RulePart_Cards import RulePart_Cards
from GRules.RulePart_Actions import RulePart_Actions
from GRules.RulePart_Following import RulePart_Following
from GRules.RulePart_Players import RulePart_Players
from GRules.RulePart_Round import RulePart_Round
from GRules.RulePart_Running import RulePart_Running

class PlayScene:
    def __init__(self, rule):
        self.__cur_round = None
        self.__history_rounds = []
        self.__players = []
        self.__rule = rule

    def is_player_in(self, player):
        return player in self.__players

    def get_players(self):
        return self.__players

    def add_player(self, player):
        if player not in self.__players:
            self.__players.append(player)
            return True
        else:
            return False

    def remove_player(self, player):
        if player in self.__players:
            self.__players.remove(player)
            return True
        return False

    def has_vacancy(self):
        return len(self.__players) < self.__rule.get_max_players_capacity()

    def prepare_start(self):
        player_part = self.__rule.get_part_by_name(RulePart_Players.PART_NAME)

    def start_game(self):
        self.prepare_start()

        run_part = self.__rule.get_part_by_name(RulePart_Running.PART_NAME)

        codeBlocks = run_part.get_code_blocks()
        for i in range(len(codeBlocks)):
            self.exe_block(codeBlocks[i])

    def exe_block(self, code_block):
        pass





