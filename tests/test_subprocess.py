import time

from croterline.context import Context
from croterline.process import SubProcess, get_ctx


def p_func(*args, **kwargs):
    print("Args", args)
    print("Kwargs", kwargs)
    i = 0
    ctx = get_ctx()
    while True:
        ctx.sub_chan << "Running" << "SubProcess"
        print("Recv from main: ", str << ctx.main_chan)
        i += 1
        if i == 5:
            ctx.sub_chan << "end"


def p_func2(*args, **kwargs):
    print("args: ", args)
    print("kwargs: ", kwargs)
    raise Exception("Test")


class TestSubProcess:
    def test_run(self):
        print("start")
        sp = SubProcess("test", p_func, Context(), 1, 2, 3, k1=1, k2=2)
        sp.start()

        while True:
            s = str << sp.ctx.sub_chan
            sp.ctx.main_chan << "Resp"
            print("Recv from sub: ", s)
            if s == "end":
                break
        print("finished")
        sp.terminate()

    def test_input(self):
        print("test_input")
        sp = SubProcess("test2", p_func2, Context(), 1, 2, 3, host=1, port=2)
        sp.start()
