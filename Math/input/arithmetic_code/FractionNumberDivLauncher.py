import inspect

from FractionNumber import FractionNumber
from Output import log_whitelist

if __name__ == '__main__':
    log_whitelist([(inspect.getfile(FractionNumber), '__truediv__')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split()  # read from stdin
        input1 = FractionNumber.from_str(args[0])
        input2 = FractionNumber.from_str(args[1])
        res = input1 / input2  # this will output markdown to stdout
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")