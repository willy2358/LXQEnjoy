
import threading
import sys
import os

import socketserver
from websocket_server import WebsocketServer

from Mains import PlayManager, Log
from Mains import CmdQueues

# Called for every client connecting (after handshake)
def new_client(client, server):
    Log.info("New web client connected and was given id %d" % client['id'])
    server.send_message(client, "Welcome!Just enjoy!")

# Called for every client disconnecting
def client_left(client, server):
    Log.info("web client(%d) disconnected" % client['id'])
    PlayManager.process_client_disconnected(client)


# Called when a client sends a message
def message_received(client, server, message):

    Log.info("web client(%d) said: %s" % (client['id'], message))
    CmdQueues.put_cmd(client, message)


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


HOST, RAWSOCK_PORT = "127.0.0.1",9229
# RAWSOCK_PORT = 9229
    # HOST, PORT = "192.168.1.57", 9229
    # HOST, PORT = "117.78.40.54", 9229
rawsock_server = socketserver.ThreadingTCPServer((HOST, RAWSOCK_PORT), MyTCPHandler)

WEBSOCK_PORT = 9228
websock_server = WebsocketServer(WEBSOCK_PORT, HOST)
websock_server.set_fn_new_client(new_client)
websock_server.set_fn_client_left(client_left)
websock_server.set_fn_message_received(message_received)

rawsock_thread = None
websock_thread = None

def run_background_servers():
    global rawsock_thread, websock_thread
    rawsock_thread = threading.Thread(group=None, target=rawsock_server.serve_forever)
    rawsock_thread.setDaemon(True)
    rawsock_thread.start()
    Log.info("raw socket is listening at {0}:{1}".format(HOST, RAWSOCK_PORT))

    websock_thread = threading.Thread(group=None, target=websock_server.run_forever)
    websock_thread.setDaemon(True)
    websock_thread.start()
    Log.info("web socket is listening at {0}:{1}".format(HOST, WEBSOCK_PORT))

if __name__ == "__main__":

    configDir = os.path.join(os.getcwd(), '..')

    PlayManager.ConfigRoot = configDir

    evt = threading.Event()
    CmdQueues.set_event(evt)

    PlayManager.initialize(evt, websock_server)

    run_background_servers()

    while True:
        line = input("input qz to exit\n")
        if line == "qz":
            rawsock_server.server_close()
            rawsock_server.shutdown()

            websock_server.server_close()
            websock_server.shutdown()

            PlayManager.exit_service()
            evt.set() # sending exit event

            Log.info("socket server closed")
            break

    Log.info("Server exited")
    sys.exit(0)


