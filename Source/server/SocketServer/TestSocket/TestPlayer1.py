import SocketClient

client = SocketClient.SocketClient("127.0.0.1", 9229)
client.run()
cmd = '{"cmdtype":"sockreq","sockreq":"join-game","userid":111,	"roomid":123333,"gameid":"m1"}'
client.send_message(cmd)
print('sent: ' + cmd)
line = input("input a command\r\n")
while line != 'exit':
    client.send_message(line)
    line = input("input a command\r\n")

"""

{"req":"join-game", "rule_id":"1212"}
{"req":"sel-act", "act-id":"1"}
{"req":"sel-act", "act-id":"1", "act-params":["poker_1_c","poker_1_d"]}

{"cmdtype":"sockreq","sockreq":"join-game","userid":123456,	"roomid":123333,"gameid":"m1"}

"""