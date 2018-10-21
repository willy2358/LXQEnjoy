import os, threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from Clients.Client import Client
from Clients.Product import Product
from Mains.PlayManager import *

__clients = []
__configDir = ""
lock = threading.Lock()


def set_config_dir(dir):
    global __configDir
    __configDir = dir


def reload():
    __clients.clear()
    for (root, _, files) in os.walk(__configDir):
        for f in files:
            if not f.endswith(".json"):
                continue

            datFile = open(os.path.join(root, f), 'r')
            jsonConf = datFile.read()
            name = jsonConf[Client.field_client_name]
            clientId = jsonConf[Client.field_client_id]
            token = jsonConf[Client.field_auth_token]
            client = Client(name, clientId, token)
            for g in jsonConf[Client.field_games]:
                gameid = g[Client.field_game_game_id]
                ruleid = g[Client.field_game_rule_id]
                rule = get_rule_by_id(ruleid)
                times = g[Client.field_game_coid_base]
                p = Product(rule, gameid, times)
                client.add_product(p)
            __clients[client.get_clientid()] = client

def start_watcher():
    reload()

    handler = Watcher()
    observer = Observer()
    observer.schedule(handler, __configDir, recursive=True)
    observer.start()
    observer.join()

def get_client(clientid):
    for c in __clients:
        if c.get_clientid() == clientid:
            return c

    return None


def is_client_valid(client, token):
    ret = False
    if lock.acquire():
        if client not in __clients:
            ret = False
        else:
            ret = (__clients[client] == token)
        lock.release()
    return ret


class Watcher(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if lock.acquire():
            reload()
            lock.release()





