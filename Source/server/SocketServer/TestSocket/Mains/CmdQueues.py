from queue import Queue

__comm_event = None

max_queue_num = 10
queues = [Queue() for i in range(max_queue_num)]

waiting_queues_idx = Queue()

in_idx = -1

def set_event(evt):
    global __comm_event
    __comm_event = evt

def put_cmd(conn, cmdText):
    global  in_idx, max_queue_num, queues, waiting_queues_idx, __comm_event
    in_idx += 1
    if in_idx >= max_queue_num:
        in_idx = 0

    queues[in_idx].put((conn, cmdText))
    waiting_queues_idx.put(in_idx)
    if __comm_event:
        __comm_event.set()

def get_cmd():
    if waiting_queues_idx.qsize() >= 1:
        idx = waiting_queues_idx.get()
        q = queues[idx]
        return q.get()
    else:
        return None, None



