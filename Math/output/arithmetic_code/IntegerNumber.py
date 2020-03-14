from __future__ import annotations

from enum import Enum

from Digit import Digit
from WholeNumber import WholeNumber


class IntegerNumber:
    @staticmethod
    def from_str(val: str) -> IntegerNumber:
        if len(val) == 0:
            raise Exception('Must contain at least 1 char')

        if val == '0':
            sign = None
            digits = str(val)
        elif val.startswith('-'):
            sign = Sign.NEGATIVE
            digits = val[1:]  # remove negative sign
        else:
            sign = Sign.POSITIVE
            digits = val

        return IntegerNumber(sign, WholeNumber(digits))

    @staticmethod
    def from_int(val: int) -> IntegerNumber:
        return IntegerNumber.from_str(str(val))

    # TODO: FIX THIS SO sign CAN BE None WHEN MAGNITUDE IS 0. 0 IS NEITHER POSITIVE OR NEGATIVE
    def __init__(self, sign: Sign, magnitude: WholeNumber):
        self.sign = sign
        self.magnitude = magnitude.copy()

    #MARKDOWN_ADD
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
    #MARKDOWN_ADD

    #MARKDOWN_SUB
    def __sub__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
        if lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE:
            if lhs.magnitude >= rhs.magnitude:
                return IntegerNumber(Sign.POSITIVE, lhs.magnitude - rhs.magnitude)
            elif lhs.magnitude < rhs.magnitude:
                return IntegerNumber(Sign.NEGATIVE, rhs.magnitude - lhs.magnitude)
        elif lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE:
            if lhs.magnitude >= rhs.magnitude:
                return IntegerNumber(Sign.NEGATIVE, lhs.magnitude - rhs.magnitude)
            elif lhs.magnitude < rhs.magnitude:
                return IntegerNumber(Sign.POSITIVE, rhs.magnitude - lhs.magnitude)
        elif lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE:
            return IntegerNumber(Sign.POSITIVE, lhs.magnitude + rhs.magnitude)
        elif lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE:
            return IntegerNumber(Sign.NEGATIVE, lhs.magnitude + rhs.magnitude)
    #MARKDOWN_SUB

    #MARKDOWN_MUL
    def __mul__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
        if (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE):
            return IntegerNumber(Sign.POSITIVE, lhs.magnitude * rhs.magnitude)
        elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE):
            return IntegerNumber(Sign.NEGATIVE, lhs.magnitude * rhs.magnitude)
    #MARKDOWN_MUL

    #MARKDOWN_DIV
    def __truediv__(lhs: IntegerNumber, rhs: IntegerNumber) -> (IntegerNumber, IntegerNumber):
        if (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE):
            (magnitude, remainder) = lhs.magnitude / rhs.magnitude
            return IntegerNumber(Sign.POSITIVE, magnitude), IntegerNumber(Sign.POSITIVE, remainder)
        elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE):
            (magnitude, remainder) = lhs.magnitude / rhs.magnitude
            return IntegerNumber(Sign.NEGATIVE, magnitude), IntegerNumber(Sign.NEGATIVE, remainder)
    #MARKDOWN_DIV

    def __str__(self: IntegerNumber) -> str:
        return ('-' if self.sign == Sign.NEGATIVE else '') + str(self.magnitude)


class Sign(Enum):
    POSITIVE = 1
    NEGATIVE = 2


if __name__ == '__main__':
    mag, rem = IntegerNumber.from_int(-30) / IntegerNumber.from_int(5)
    print(f'{mag}R{rem}')
