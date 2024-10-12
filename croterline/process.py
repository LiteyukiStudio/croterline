from multiprocessing import Process as _Process
from typing import Callable, Any

from croterline.context import Context
from croterline.utils import IsMainProcess

type ProcessFuncType = Callable[[tuple[Any, ...], dict[str, Any]], None]

_processes: dict[str, "SubProcess"] = {}

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
        set_process(self.name, self)

    def terminate(self):
        self.process.terminate()
        set_process(self.name, None)

    def join(self, timeout: float = 0):
        self.process.join(timeout=timeout)
        set_process(self.name, None)


def set_process(name: str, process: SubProcess | None):
    _processes[name] = process


def get_process(name: str) -> SubProcess | None:
    """
    获取进程对象，在主进程中调用，只可在主进程调用
    Args:
        name: 进程名称
    Returns:
        进程对象
    """
    if not IsMainProcess:
        raise RuntimeError(
            "get_process with specific name can only be called in the main process."
        )
    return _processes.get(name, None)


def get_ctx(name: str | None = None) -> Context | None:
    """
    获取进程上下文，在主进程中调用需指定进程名称，若在子进程中调用则无需指定进程名称
    Returns:
        进程上下文
    """
    if name is not None:
        if not IsMainProcess:
            raise RuntimeError(
                "get_ctx with specific name can only be called in the main process."
            )
        return _processes.get(name, None).ctx
    else:
        if IsMainProcess:
            raise RuntimeError(
                "get_ctx without name can only be called in the sub process."
            )
        return _current_ctx


def _wrapper(func: ProcessFuncType, ctx: Context, *args, **kwargs):
    global _current_ctx

    _current_ctx = ctx
    func(*args, **kwargs)
