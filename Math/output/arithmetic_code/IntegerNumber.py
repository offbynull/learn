from __future__ import annotations

from enum import Enum

from Digit import Digit
from WholeNumber import WholeNumber


class IntegerNumber:
    @staticmethod
    def from_int(val: int) -> IntegerNumber:
        if val == 0:
            sign = None
            digits = str(val)
        elif val < 0:
            sign = Sign.NEGATIVE
            digits = str(val)[1:]  # remove negative sign
        else:
            sign = Sign.POSITIVE
            digits = str(val)

        digits = list(map(lambda i: Digit(int(i)), digits))
        return IntegerNumber(sign, WholeNumber(digits))

    def __init__(self, sign: Sign, magnitude: WholeNumber):
        self.sign = sign
        self.magnitude = magnitude.copy()

    def __add__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
        if lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE:
            return IntegerNumber(Sign.POSITIVE, lhs.magnitude + rhs.magnitude)
        elif lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE:
            return IntegerNumber(Sign.NEGATIVE, lhs.magnitude + rhs.magnitude)
        elif lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE:
            if lhs.magnitude >= rhs.magnitude:
                return IntegerNumber(Sign.POSITIVE, lhs.magnitude - rhs.magnitude)
            else:
                return IntegerNumber(Sign.NEGATIVE, rhs.magnitude - lhs.magnitude)
        elif lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE:
            if lhs.magnitude >= rhs.magnitude:
                return IntegerNumber(Sign.NEGATIVE, lhs.magnitude - rhs.magnitude)
            else:
                return IntegerNumber(Sign.POSITIVE, rhs.magnitude - lhs.magnitude)

    def __str__(self: WholeNumber) -> str:
        return ('-' if self.sign == Sign.NEGATIVE else '') + str(self.magnitude)


class Sign(Enum):
    POSITIVE = 1
    NEGATIVE = 2


if __name__ == '__main__':
    print(f'{IntegerNumber.from_int(6) + IntegerNumber.from_int(4)}')
    print(f'{IntegerNumber.from_int(6) + IntegerNumber.from_int(-4)}')
    print(f'{IntegerNumber.from_int(-6) + IntegerNumber.from_int(4)}')
    print(f'{IntegerNumber.from_int(-6) + IntegerNumber.from_int(-4)}')
    print(f'{IntegerNumber.from_int(-4) + IntegerNumber.from_int(6)}')
