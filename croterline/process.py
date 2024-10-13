from multiprocessing import Process as _Process
from typing import Callable, Any

from mypy.nodes import TypeAlias

from croterline.context import Context
from croterline.utils import IsMainProcess

ProcessFuncType: TypeAlias = Callable[[tuple[Any, ...], dict[str, Any]], None]

_current_ctx: "Context | None" = None  # 注入当前进程上下文


class SubProcess:
    def __init__(
        self, name: str, func: ProcessFuncType, ctx: Context = Context, *args, **kwargs
    ):
        self.name = name
        self.func = func
        self.ctx = ctx
        self.args = args
        self.kwargs = kwargs
        self.process: _Process | None = None

    def start(self):
        self.process = _Process(
            target=_wrapper,
            args=(self.func, self.ctx, *self.args),
            kwargs=self.kwargs,
        )
        self.process.start()

    def terminate(self):
        self.process.terminate()

    def join(self, timeout: float = 0):
        self.process.join(timeout=timeout)


def get_ctx() -> Context | None:
    """
    获取进程上下文，在主进程中调用需指定进程名称，若在子进程中调用则无需指定进程名称
    Returns:
        进程上下文
    """
    if IsMainProcess:
        raise RuntimeError(
            "get_ctx without name can only be called in the sub process."
        )
    return _current_ctx


def _wrapper(func: ProcessFuncType, ctx: Context, *args, **kwargs):
    print("args", args)
    print("kwargs", kwargs)
    global _current_ctx

    _current_ctx = ctx
    func(*args, **kwargs)
