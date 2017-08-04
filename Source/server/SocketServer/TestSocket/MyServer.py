import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        print(self.client_address)
        #conn.sendall('I am multi thread')
        Flag = True
        while Flag:
            data = conn.recv(1024)
            print('received:' + data.decode())
            if data == 'exit':
                Flag = False
            else:
                #bdata = bytes(str(data), encoding="utf-8")
		#bdata = bytes(data,encode='utf-8')
                #conn.sendall('input:' + bdata)
                resp = 'your input :' + data.decode()
                print('response:' + resp)
                try:
                    conn.sendall(resp.encode(encoding="utf-8"))
                except Exception as x:
                    print('Send exception:' + x.message)
                        
                
                
        
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    
if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9229

    # Create the server, binding to localhost on port 9999
    #server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server = socketserver.ThreadingTCPServer((HOST,PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print('run at:' + str(PORT))
    server.serve_forever()
