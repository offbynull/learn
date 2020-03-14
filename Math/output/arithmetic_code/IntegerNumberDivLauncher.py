import inspect

from IntegerNumber import IntegerNumber
from Output import log_whitelist

if __name__ == '__main__':
    log_whitelist([(inspect.getfile(IntegerNumber), '__truediv__')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split()  # read from stdin
        input1 = IntegerNumber.from_str(args[0])
        input2 = IntegerNumber.from_str(args[1])
        res = input1 / input2  # this will output markdown to stdout
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")