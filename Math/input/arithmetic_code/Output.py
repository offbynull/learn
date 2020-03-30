from __future__ import annotations

from enum import Enum
import inspect
from typing import List, Tuple, Optional

save_states: List[int] = []
indent_offset: int = -2
whitelist: List[Tuple[str, str]] = []


def log_indent():
    global indent_offset
    indent_offset += 2


def log_unindent():
    global indent_offset
    indent_offset -= 2


def log_push_indent_state():
    global indent_offset
    save_states.append(indent_offset)


def log_pop_indent_state():
    global indent_offset, save_states
    indent_offset = save_states.pop()


def log_whitelist(allowed: List[Tuple[str, str]]):
    global whitelist
    whitelist = allowed


def log(data: str):
    global indent_offset, whitelist

    if not (inspect.stack()[1].filename, inspect.stack()[1].function) in whitelist:
        return

    data = (' ' * indent_offset) + ' * ' + data
    print(data)


def log_decorator(func):
    def inner(*args, **kwargs):
        log_push_indent_state()
        try:
            log_indent()
            return func(*args, **kwargs)
            log_unindent()
        finally:
            log_pop_indent_state()
    return inner


if __name__ == '__main__':
    output = inspect.stack()
    print(str(output[0].function))
