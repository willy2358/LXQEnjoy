from GCore.Statement import Statement

class ExitRound(Statement):
    def __init__(self):
        super(ExitRound, self).__init__()

    def gen_runtime_obj(self, scene):
        def exit_round_func():
            scene.set_exit_cur_round()
        return exit_round_func