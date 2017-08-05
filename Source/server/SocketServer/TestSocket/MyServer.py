import socketserver

import Player

waiting_players = {}


class MyTCPHandler(socketserver.BaseRequestHandler):
    __Players = []

    def handle(self):
        conn = self.request
        player = Player.Player(conn)
        MyTCPHandler.__Players.append({conn, player})
        print('client:' + str(len(MyTCPHandler.__Players)))
        print(MyTCPHandler.__Players)

        print(self.client_address)

        flag = True
        while flag:
            data = conn.recv(1024)
            self.dispatch_player_commands(conn, data);
            print('received:' + data.decode())
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

    def dispatch_player_commands(self, conn, comm_text):
        parts = comm_text.split('#')
        if len(parts) == 2:
            if parts[0].lower() == "play_rule":
                self.process_command_play_rule(conn, comm_text)
            if parts[0].lower() == "play_card":
                self.process_command_play_card(conn, comm_text)
            if parts[0].lower() == "play_leave":
                self.process_command_play_leave(conn)

    def process_command_play_rule(self, command_text):
        pass

    def process_command_play_card(self, conn, command_text):
        pass

    def process_command_play_leave(self, conn):
        pass


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9229

    # Create the server, binding to localhost on port 9999
    # server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server = socketserver.ThreadingTCPServer((HOST,PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print('run at:' + str(PORT))
    server.serve_forever()
