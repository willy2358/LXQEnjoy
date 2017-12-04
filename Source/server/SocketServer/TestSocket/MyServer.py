import socketserver

import PlayManager
import PlayerClient


class MyTCPHandler(socketserver.StreamRequestHandler):
    __Players = []

    def handle(self):
        conn = self.request

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("client closed")
                    PlayManager.process_client_disconnected(conn)
                    break
                else:
                    print('received:' + data.decode())
                    PlayManager.dispatch_player_commands(conn, data.decode())
            except Exception as e:
                print(e)

if __name__ == "__main__":

    PlayManager.initialize()

    HOST, PORT = "127.0.0.1", 9229

    # Create the server, binding to localhost on port 9999
    # server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server = socketserver.ThreadingTCPServer((HOST,PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print('run at:' + str(PORT))
    try:
        server.serve_forever()
    except:
        server.server_close()
