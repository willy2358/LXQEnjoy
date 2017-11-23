import SocketClient

client = SocketClient.SocketClient("127.0.0.1", 9229)
client.run()
cmd = '{"cmdtype":"sockreq","sockreq":"join-game","userid":333,	"roomid":123333,"gameid":"m1"}'
client.send_message(cmd)
print('sent: ' + cmd)
line = input("input a command\r\n")
while line != 'exit':
    client.send_message(line)
    line = input("input a command\r\n")

"""


{"cmdtype":"sockreq","sockreq":"join-game","userid":123456,	"roomid":123333,"gameid":"m1"}

"""