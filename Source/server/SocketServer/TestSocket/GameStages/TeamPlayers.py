from GameStages.GameStage import GameStage


class TeamPlayers(GameStage):
    COMMAND_BANK_CARDS = "bank-cards"

    def __init__(self, rule):
        super(TeamPlayers, self).__init__(rule)
        self.__players_teamed = False

    def is_completed(self):
        return self.__players_teamed

    def begin(self):
        bank_player = self.get_my_round().get_bank_player()
        if bank_player:
            cards = self.get_my_round().get_cards_for_banker()
            cmd_obj = {"cmd": TeamPlayers.COMMAND_BANK_CARDS, "cards": cards}
            bank_player.send_server_command(cmd_obj)
            self.__players_teamed = True
            self.get_my_round().test_and_update_current_stage()
        else:
            self.get_my_round().process_no_bank_player()



