import SocketClient

client = SocketClient.SocketClient("127.0.0.1", 9229)
client.run()
line = input("input a command\r\n")
while line != 'exit':
    client.send_message(line)
    line = input("input a command\r\n")

"""

{"req":"join-game", "rule_id":"1212"}
{"req":"player-resp","resp":"resp-deal_finish"}
{"req":"call", "act-id":"2"}

cards_sorted
select_call#{"action_id":"1"}
"""