
import threading
import sys
import os

import socketserver

from Mains import PlayManager, Log
from Mains import CmdQueues


class MyTCPHandler(socketserver.StreamRequestHandler):
    __Players = []

    def handle(self):
        conn = self.request
        try:
            conn.sendall("Welcome!Just enjoy!".encode(encoding="utf-8"))
        except Exception as ex:
            Log.exception(ex)

        while True:
            try:
                # time.sleep(0.2)
                data = conn.recv(1024)
                if not data:
                    Log.debug("client closed")
                    PlayManager.process_client_disconnected(conn)
                    break
                else:
                    Log.debug('received:{0}, in thread:{1}'.format(data.decode(), threading.get_ident()))
                    # PlayManager.dispatch_player_commands(conn, data.decode())
                    CmdQueues.put_cmd(conn, data.decode())
            except Exception as e:
                PlayManager.process_client_disconnected(conn)
                Log.exception(e)
                break


HOST, PORT = "127.0.0.1", 9229
    # HOST, PORT = "192.168.1.57", 9229
    # HOST, PORT = "117.78.40.54", 9229
server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

thread = None

def run_background_server():
    global thread
    thread = threading.Thread(group=None, target=server.serve_forever)
    thread.setDaemon(True)
    thread.start()

if __name__ == "__main__":

    configDir = os.path.join(os.getcwd(), '..')

    PlayManager.ConfigRoot = configDir

    evt = threading.Event()
    CmdQueues.set_event(evt)

    PlayManager.initialize(evt)

    run_background_server()

    while True:
        line = input("input qz to exit\n")
        if line == "qz":
            server.server_close()
            server.shutdown()
            PlayManager.exit_service()
            evt.set() # sending exit event

            Log.info("socket server closed")
            break

    Log.info("Server exited")
    sys.exit(0)


