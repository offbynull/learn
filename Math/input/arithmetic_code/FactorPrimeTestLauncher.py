import inspect

import Factor
from Factor import factor_naive, is_prime
from WholeNumber import WholeNumber
from Output import log_whitelist

if __name__ == '__main__':
    log_whitelist([(inspect.getfile(Factor), 'is_prime')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split()  # read from stdin
        input1 = WholeNumber(args[0])
        res = is_prime(input1)  # this will output markdown to stdout
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")
7