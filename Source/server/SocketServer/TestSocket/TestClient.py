import SocketClient

client = SocketClient.SocketClient("127.0.0.1", 9229)
client.run()
line = input("input a command\r\n")
while line != 'exit':
    client.send_message(line)
    line = input("input a command\r\n")




