from typing import Callable, Any

from magicoca.chan import Chan


class Context:
    def __init__(self):
        """
        main_chan: Chan[Any] = main to sub
        sub_chan: Chan[Any] = sub to main
        哪个进程发送用哪个
        """
        self.main_chan: Chan[Any] = Chan[Any]()  # main to sub
        self.sub_chan: Chan[Any] = Chan[Any]()  # sub to main

    def set_value(self, key: str, value: Any):
        setattr(self, key, value)

    def get_value(self, key: str) -> Any:
        return getattr(self, key)
