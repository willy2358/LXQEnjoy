from Test import SocketClient
from Mains import InterProtocol
import json
import time


roomid = "0"
userid = 4444
gameid = "shengji001"
# roomid = 888
# client = SocketClient.SocketClient("117.78.40.54", 9229)
cmd_opts = None
def_cmd = None

def join_game():
    mycmd = {
        "cmdtype":"sockreq",
        "sockreq":"join-game",
        "userid":userid,
        "roomid":roomid,
        "gameid":gameid,
        "clientid": "00001",
        "token": client.get_token(),
        "seatid":1
    }
    myCmd_str = json.dumps(mycmd)
    client.send_message(myCmd_str)
    print('sent: ' + myCmd_str)

def msg_callback(jsonObj):
    global cmd_opts, def_cmd
    if  "sockresp" in jsonObj and jsonObj["sockresp"] == "reg-player" and jsonObj["result"] == "OK":
        time.sleep(0.5)
        join_game()
    if "sockpush" in jsonObj and jsonObj["sockpush"] == "cmd-opts":
        cmd_opts = jsonObj["cmd-opts"]
        def_cmd = jsonObj["def-cmd"]


client = SocketClient.SocketClient("127.0.0.1", 9229, msg_callback)
client.run()

cmd = {
        "cmdtype":"sockreq",
        "sockreq":"reg-player",
        "userid":userid,
        "clientid":"00001",
        "token":"prs35tqjMI3VUn6M6lyyPLcj84Q"
    }

cmd_str = json.dumps(cmd)
client.send_message(cmd_str)


while True:
    # cmd_args = json.dumps(cmds) + "\r\n"
    line = input("selcmd:1,2,3; play cards: s1,s2,c3\r\n")
    # client.send_message(line)
    # continue
    packet = None
    if line.isnumeric():
        packet = {
            InterProtocol.cmd_type: InterProtocol.sock_req_cmd,
            InterProtocol.sock_req_cmd: InterProtocol.client_req_type_exe_cmd,
            InterProtocol.user_id: userid,
            InterProtocol.room_id: roomid,
            InterProtocol.game_id: gameid,
            "clientid": "00001",
            "token": client.get_token(),
            InterProtocol.client_req_exe_cmd: cmd_opts[int(line)-1]["cmd"],
            InterProtocol.client_req_cmd_param: cmd_opts[int(line)-1]["cmd-param"]
        }
        str_obj = json.dumps(packet)
        client.send_message(str_obj)
    elif line == "get-cards":
        packet = {
            InterProtocol.cmd_type: InterProtocol.sock_req_cmd,
            InterProtocol.sock_req_cmd: InterProtocol.client_req_get_cards,
            InterProtocol.user_id: userid,
            InterProtocol.room_id: roomid,
            InterProtocol.game_id: gameid,
            "clientid": "00001",
            "token": client.get_token(),
        }
        str_obj = json.dumps(packet)
        client.send_message(str_obj)
    elif ':' in line:
        parts = line.split(':')
        cmd = parts[0]
        cmd_param = parts[1].split(',')
        if cmd == "play-cards":
            packet = {
                InterProtocol.cmd_type: InterProtocol.sock_req_cmd,
                InterProtocol.sock_req_cmd: InterProtocol.client_req_play_cards,
                InterProtocol.user_id: userid,
                InterProtocol.room_id: roomid,
                InterProtocol.game_id: gameid,
                "clientid": "00001",
                "token": client.get_token(),
                InterProtocol.cmd_data_cards: cmd_param,
            }
            str_obj = json.dumps(packet)
            client.send_message(str_obj)
        else:
            packet = {
                InterProtocol.cmd_type: InterProtocol.sock_req_cmd,
                InterProtocol.sock_req_cmd: InterProtocol.client_req_type_exe_cmd,
                InterProtocol.user_id: userid,
                InterProtocol.room_id: roomid,
                InterProtocol.game_id: gameid,
                "clientid": "00001",
                "token": client.get_token(),
                InterProtocol.client_req_exe_cmd: cmd if not cmd.isnumeric() else cmd_opts[int(cmd) - 1]["cmd"],
                InterProtocol.client_req_cmd_param: cmd_param
            }
            str_obj = json.dumps(packet)
            client.send_message(str_obj)
