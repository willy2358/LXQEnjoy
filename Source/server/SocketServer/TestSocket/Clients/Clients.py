import os, threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

__clients = []
__configDir = ""
lock = threading.Lock()


def set_config_dir(dir):
    __configDir = dir


def reload():
    __clients.clear()
    for (root, _, files) in os.walk(__configDir):
        for f in files:
            if not f.endswith(".dat"):
                continue

            datFile = open(os.path.join(root, f), 'r')
            line = datFile.read()
            ps = line.split(':')
            if len(ps) != 2:
                continue
            __clients[ps[0]] = ps[1]


def start_watcher():
    reload()

    handler = Watcher()
    observer = Observer()
    observer.schedule(handler, __configDir, recursive=True)
    observer.start()
    observer.join()


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





