import inspect

import CommonDivisibilityTest
from CommonDivisibilityTest import common_divisibility_test
from Output import log_whitelist
from WholeNumber import WholeNumber

if __name__ == '__main__':
    log_whitelist([(inspect.getfile(CommonDivisibilityTest), 'common_divisibility_test')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split()  # read from stdin
        input1 = WholeNumber(args[0])
        res = common_divisibility_test(input1)
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")