import inspect

import GreatestCommonDivisor
from GreatestCommonDivisor import gcd_naive
from Output import log_whitelist
from WholeNumber import WholeNumber

if __name__ == '__main__':
    log_whitelist([(inspect.getfile(GreatestCommonDivisor), 'gcd_naive')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split()  # read from stdin
        input1 = WholeNumber.from_str(args[0])
        input2 = WholeNumber.from_str(args[1])
        res = gcd_naive(input1, input2)  # this will output markdown to stdout
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")
