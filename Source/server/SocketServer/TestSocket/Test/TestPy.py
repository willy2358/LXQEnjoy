
waiting = False

def func1():
    print("func1")

def func2():
    print("func2")

def func3():
    print("func3")
    global waiting
    waiting = True

def func4():
    print("func4")
    myfs = [func41, func42, func43, func44]
    for f in myfs:
        if waiting:
            return
        yield f

    # yield from myfs
    # for f in myfs:
    #     yield f

def func41():
    print("func41")

def func42():
    print("func42")

def func43():
    print("func43")

def func44():
    print("func44")

def func5():
    print("func5")

def func6():
    print("func6")


def main_funcs():
    yield from sub_funcs()

def sub_funcs():
    myfuncs = [func1, func2, func3, func4, func5, func6]
    for f in myfuncs:
        if f == func4:
            yield from f()
        else:
            yield f


if __name__ == "__main__":
    print("start")

    # for f in main_funcs():
    #     f()
    print(isinstance(main_funcs()))