import PlayManager

from datetime import datetime,timedelta

class Player:
    def __init__(self, userid):
        self.__userid = userid
        self.__token = None
        self.__sock_conn = None
        self.__closet = None
        self.__last_alive_time = datetime.now()

    def get_userid(self):
        return self.__userid

    def get_token(self):
        return self.__token

    def get_sock_conn(self):
        return self.__sock_conn

    def get_closet(self):
        return self.__closet

    def set_sock_conn(self, conn):
        self.__sock_conn = conn

    def set_token(self, token):
        self.__token = token

    def set_closet(self, closet):
        return self.__closet

    def update_last_alive(self):
        self.__last_alive_time = datetime.now()

    def response_success_pack(self, pack):
        PlayManager.send_pack_to_client(self.__sock_conn, pack)

    def response_err_pack(self, cmd, err_code):
        PlayManager.send_err_pack_to_client(self.__sock_conn, cmd, err_code)