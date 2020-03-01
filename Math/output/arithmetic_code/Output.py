import inspect
from typing import List

indent_offset: int = -2
first_line: bool = True
whitelist: List[str] = []

def log_indent():
    global indent_offset, first_line
    indent_offset += 2
    first_line = True

def log_unindent():
    global indent_offset, first_line
    indent_offset -= 2

def log_whitelist(allowed: List[str]):
    global whitelist
    whitelist = allowed

def log(data: str):
    global indent_offset, first_line, whitelist

    if not inspect.stack()[1].function in whitelist:
        return

    data = (' ' * indent_offset) + ' * ' + data
    print(data)


if __name__ == '__main__':
    output = inspect.stack()
    print(str(output))