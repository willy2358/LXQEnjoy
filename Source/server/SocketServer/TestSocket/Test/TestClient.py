from Test import SocketClient
from Mains import InterProtocol
import json

# roomid = "LX888"
# userid = 111
# gameid = 111
players = [111,222,333]
# roomid = 888
# client = SocketClient.SocketClient("117.78.40.54", 9229)
client = SocketClient.SocketClient("127.0.0.1", 9229)
client.run()

for userid in players:
    print('registering:' + str(userid))
    cmd = {
        "cmdtype":"sockreq",
        "sockreq":"reg-player",
        "userid":userid,
        "clientid":"00001",
        "token":"prs35tqjMI3VUn6M6lyyPLcj84Q"
    }
    cmd_str = json.dumps(cmd)
    client.send_message(cmd_str)
    line = input("press any key to register next player\r\n")


