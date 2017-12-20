import SocketClient
import InterProtocol
import json

client = SocketClient.SocketClient("127.0.0.1", 9229)
client.run()
cmd = '{"cmdtype":"sockreq","sockreq":"join-game","userid":222,	"roomid":123333,"gameid":"m1"}'
client.send_message(cmd)
print('sent: ' + cmd)
cmds = {
    "0":InterProtocol.majiang_player_act_zimo,
    "1":InterProtocol.majiang_player_act_hu,
    "2":InterProtocol.majiang_player_act_gang,
    "3":InterProtocol.majiang_player_act_peng,
    "4":InterProtocol.majiang_player_act_chi,
    "5":InterProtocol.majiang_player_act_pass,
    "6":InterProtocol.majiang_player_act_play_card,
    "7":InterProtocol.majiang_player_act_mopai
}

while True:
    cmd_args = json.dumps(cmds) + "\r\n"
    line = input(cmd_args)
    ps = line.split(',')
    cmd = ps[0]
    if cmd == 8 or cmd == "exit":
        break
    cmd_param = int(ps[1]) if len(ps) > 1 else None
    if cmd in cmds:
        packet = {
            InterProtocol.cmd_type: InterProtocol.sock_req_cmd,
            InterProtocol.sock_req_cmd:InterProtocol.client_req_type_exe_cmd,
            InterProtocol.user_id:222,
            InterProtocol.room_id:123333,
            InterProtocol.client_req_exe_cmd:cmds[cmd],
            InterProtocol.client_req_cmd_param:cmd_param
        }
        str_obj = json.dumps(packet)
        client.send_message(str_obj)

"""
{"cmdtype":"sockreq","sockreq":"join-game","userid":123456,	"roomid":123333,"gameid":"m1"}

"""