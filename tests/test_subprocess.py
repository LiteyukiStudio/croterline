import time

from croterline.context import Context
from croterline.process import SubProcess, get_ctx


def p_func(*args, **kwargs):
    i = 0
    ctx = get_ctx()
    while True:
        ctx.sub_chan << "Running" << "SubProcess"
        print("Recv from main: ", str << ctx.main_chan)
        i += 1
        if i == 5:
            ctx.sub_chan << "end"


class TestSubProcess:
    def test_run(self):
        print("start")
        sp = SubProcess("test", p_func, Context())
        sp.start()

        while True:
            s = str << sp.ctx.sub_chan
            sp.ctx.main_chan << "Resp"
            print("Recv from sub: ", s)
            if s == "end":
                break
        print("finished")
        sp.terminate()

    def test_decorator(self):
        pass
