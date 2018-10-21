import socket
import sys
import threading
import json

import Mains.InterProtocol as InterProtocol


def wait_sock_receive(sock_client):
    while sock_client.is_run():
        try:
            buf = sock_client.socket().recv(128)
            data = buf.decode('utf-8')
            print('Received:' + data + "\r\n")
        except Exception as ex:
            print(ex)
            #_isRun = False

    try:
        sock_client.socket.close()
    except Exception as ex:
        print(ex)


class SocketClient:
    def __init__(self, address, port):
        self._address = address
        self._port = port
        self.__isRun = False
        self.__mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__receiveThread = None
        self.__token = ""

    def run(self):
        try:
            self.__mySock.connect((self._address, self._port))
            self.__isRun = True
            self.__receiveThread = threading.Thread(group=None, target=self.__waitSockReceive__)
            self.__receiveThread.setDaemon(True)
            self.__receiveThread.start()
            print(self.__receiveThread)
        except Exception as e:
            print(e)
            raise e

    def send_message(self, msg):
        try:
            self.__mySock.sendall(msg.encode('utf-8'))
        except Exception as e:
            print(e)

    def __waitSockReceive__(self):
        while self.__isRun:
            try:
                buf = self.__mySock.recv(1024)
                if not buf:
                    print("client closed")
                    break
                data = buf.decode('utf-8')
                parts = data.split("LXQ<(:");
                for p in parts:
                    if len(p) < 5:
                        continue
                    p = p.strip(":)>QXL")
                    print('Received:' + p)
                    if not p.startswith('{'):
                        continue
                    j_obj = json.loads(p)
                    if j_obj[InterProtocol.sock_resp] == InterProtocol.client_req_cmd_reg_player:
                        if InterProtocol.resp_player in j_obj:
                            self.__token = j_obj[InterProtocol.resp_player][InterProtocol.authed_token]

                        # print("\r\n")

            except Exception as ex:
                print(ex)
                self.__isRun = False

        try:
            self.__mySock.close()
        except Exception as ex:
            print(ex)

    def is_run(self):
        return self.__isRun

    def socket(self):
        return self.__mySock

    def get_token(self):
        return self.__token

    def stop(self):

        self.__isRun = False
