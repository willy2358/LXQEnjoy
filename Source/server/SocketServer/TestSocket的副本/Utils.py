

def list_remove_parts(src_list, parts):
    for i in parts:
        if i in src_list:
            src_list.remove(i)

    return src_list
