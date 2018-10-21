import SocketClient
from Mains import InterProtocol
import json

roomid = "LX888"
userid = 111
gameid = 111
# roomid = 888
# client = SocketClient.SocketClient("117.78.40.54", 9229)
client = SocketClient.SocketClient("127.0.0.1", 9229)
client.run()

# cmd = '{"cmdtype":"sockreq","sockreq":"enter-room","userid":111,"roomid":' +'"' + roomid +'","gameid":"m1"}'
# cmd = '{"cmdtype":"sockreq","sockreq":"enter-room","userid":111,"roomid":' + roomid +',"gameid":"m1"}'
cmd = {
    "cmdtype":"sockreq",
    "sockreq":"enter-room",
    "userid":userid,
    "roomid":roomid,
    "gameid":gameid
}
cmd_str = json.dumps(cmd)
client.send_message(cmd_str)


line = input("press any key to join game\r\n")

# cmd = '{"cmdtype":"sockreq","sockreq":"join-game","userid":111,	"roomid":' + roomid +',"gameid":"m1"}'
cmd = {
    "cmdtype":"sockreq",
    "sockreq":"join-game",
    "userid":userid,
    "roomid":roomid,
    "gameid":gameid,
    "seatid":3
}
cmd_str = json.dumps(cmd)
client.send_message(cmd_str)
print('sent: ' + cmd_str)
cmds = {
    "0": InterProtocol.majiang_player_act_zimo,
    "1": InterProtocol.majiang_player_act_hu,
    "2": InterProtocol.majiang_player_act_gang,
    "3": InterProtocol.majiang_player_act_peng,
    "4": InterProtocol.majiang_player_act_chi,
    "5": InterProtocol.majiang_player_act_pass,
    "6": InterProtocol.majiang_player_act_play_card,
    "7": InterProtocol.majiang_player_act_mopai,
    "8":"exit"
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
            InterProtocol.sock_req_cmd: InterProtocol.client_req_type_exe_cmd,
            InterProtocol.user_id:userid,
            InterProtocol.room_id:roomid,
            InterProtocol.game_id:gameid,
            InterProtocol.client_req_exe_cmd:cmds[cmd],
            InterProtocol.client_req_cmd_param:[cmd_param]
        }
        if cmd == "6":
            packet = {
                InterProtocol.cmd_type: InterProtocol.sock_req_cmd,
                InterProtocol.sock_req_cmd: InterProtocol.client_req_play_cards,
                InterProtocol.user_id: userid,
                InterProtocol.room_id: roomid,
                InterProtocol.game_id:gameid,
                InterProtocol.cmd_data_cards: [cmd_param],
            }

        str_obj = json.dumps(packet)
        client.send_message(str_obj)
