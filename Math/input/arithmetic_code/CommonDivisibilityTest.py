from __future__ import annotations

from typing import Set, List

from Digit import Digit
from WholeNumber import WholeNumber


def common_divisibility_test(num: WholeNumber) -> Set[WholeNumber]:
    ret: Set[WholeNumber] = set()

    last_digit: WholeNumber = WholeNumber(num.digits[0])  # last digit is always at 0 idx

    # is divisible by 2?
    if last_digit == WholeNumber(0) \
            or last_digit == WholeNumber(2) \
            or last_digit == WholeNumber(4) \
            or last_digit == WholeNumber(6) \
            or last_digit == WholeNumber(8):
        print(f" * {num} is divisible by 2\n")
        ret.add(WholeNumber(2))
    else:
        print(f" * {num} is NOT divisible by 2\n")

    # is divisible by 5?
    if last_digit == WholeNumber(0) \
            or last_digit == WholeNumber(5):
        print(f" * {num} is divisible by 5\n");
        ret.add(WholeNumber(5))
    else:
        print(f" * {num} is NOT divisible by 5\n");

    # is divisible by 10?
    if last_digit == WholeNumber(0):
        print(f" * {num} is divisible by 10\n");
        ret.add(WholeNumber(10))
    else:
        print(f" * {num} is NOT divisible by 10\n");

    # is divisible by 3?
    reduced_num: WholeNumber = num.copy()
    while True:
        digits = reduced_num.digits
        if len(digits) == 1:
            break
        reduced_num = sum([WholeNumber(d) for d in digits], WholeNumber(0))

    if reduced_num == WholeNumber(3) \
            or reduced_num == WholeNumber(6) \
            or reduced_num == WholeNumber(9):
        print(f" * {num} is divisible by 3\n")
        ret.add(WholeNumber(3))
    else:
        print(f" * {num} is NOT divisible by 3\n")

    # is divisible  by 6?
    if WholeNumber(2) in ret and WholeNumber(3) in ret:
        print(f" * {num} is divisible by 6\n")
        ret.add(WholeNumber(6))
    else:
        print(f" * {num} is NOT divisible by 6\n")

    return ret


if __name__ == '__main__':
    print(f'{common_divisibility_test(WholeNumber(15))}')
