from GCore.Statement import Statement
import Mains.Log as Log

class ProcRef(Statement):
    def __init__(self, procName):
        super(ProcRef, self).__init__()
        self.__proc_name = procName

    def gen_runtime_obj(self, scene):

        def call_proc():
            try:
                Log.debug("Executing:{0} ....".format(self.get_step()))
                scene.call_proc(self.__proc_name, [])

            except Exception as ex:
                Log.exception(ex)

        return call_proc