import socketserver

import PlayManager
import PlayerClient

class MyTCPHandler(socketserver.BaseRequestHandler):
    __Players = []

    def handle(self):
        conn = self.request
        # player = Player.Player(conn)
        # MyTCPHandler.__Players.append({conn, player})

        PlayManager.add_player_client(conn)

        flag = True
        while flag:
            data = conn.recv(1024)
            print('received:' + data.decode())
            PlayManager.dispatch_player_commands(conn, data);

            # print(conn)
            # print(MyTCPHandler.__Clients.index(conn))
            # if data == 'exit':
            #     flag = False
            # else:
            #     resp = 'your input :' + data.decode()
            #     print('response:' + resp)
            #     try:
            #         conn.sendall(resp.encode(encoding="utf-8"))
            #     except Exception as x:
            #         print('Send exception:' + x.message)



if __name__ == "__main__":

    PlayManager.init_play_rules()

    HOST, PORT = "127.0.0.1", 9229

    # Create the server, binding to localhost on port 9999
    # server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server = socketserver.ThreadingTCPServer((HOST,PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print('run at:' + str(PORT))
    server.serve_forever()
