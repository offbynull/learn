from __future__ import annotations

from enum import Enum
from typing import Union

from WholeNumber import WholeNumber


class IntegerNumber:
    @staticmethod
    def from_str(val: str) -> IntegerNumber:
        if len(val) == 0:
            raise Exception('Must contain at least 1 char')

        if val.startswith('-'):
            sign = Sign.NEGATIVE
            digits = val[1:]  # remove negative sign
        else:
            sign = Sign.POSITIVE
            digits = val

        magnitude = WholeNumber(digits)

        if magnitude == WholeNumber(0):
            sign = None

        return IntegerNumber(sign, magnitude)

    @staticmethod
    def from_int(val: int) -> IntegerNumber:
        return IntegerNumber.from_str(str(val))

    # TODO: FIX THIS SO sign CAN BE None WHEN MAGNITUDE IS 0. 0 IS NEITHER POSITIVE OR NEGATIVE
    def __init__(self, sign: Union[Sign, None], magnitude: WholeNumber):
        self.sign = sign
        self.magnitude = magnitude.copy()

        if magnitude == WholeNumber(0) and sign is not None:
            raise Exception('Magnitude of 0 cannot have a sign')

    def copy(self: IntegerNumber):
        return IntegerNumber(self.sign, self.magnitude)

    #MARKDOWN_ADD
    def __add__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
        if lhs.magnitude == WholeNumber(0):  # 0 + a = a, why add this? it simplifies logic below because 0 has no sign
            return rhs.copy()
        if rhs.magnitude == WholeNumber(0):  # a + 0 = a, why add this? it simplifies logic below because 0 has no sign
            return lhs.copy()

        if lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE:
            sign = Sign.POSITIVE
            magnitude = lhs.magnitude + rhs.magnitude
        elif lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE:
            sign = Sign.NEGATIVE
            magnitude = lhs.magnitude + rhs.magnitude
        elif lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE:
            if lhs.magnitude >= rhs.magnitude:
                sign = Sign.POSITIVE
                magnitude = lhs.magnitude - rhs.magnitude
            else:
                sign = Sign.NEGATIVE
                magnitude = rhs.magnitude - lhs.magnitude
        elif lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE:
            if lhs.magnitude >= rhs.magnitude:
                sign = Sign.NEGATIVE
                magnitude = lhs.magnitude - rhs.magnitude
            else:
                sign = Sign.POSITIVE
                magnitude = rhs.magnitude - lhs.magnitude

        if magnitude == WholeNumber(0):
            sign = None

        return IntegerNumber(sign, magnitude)
    #MARKDOWN_ADD

    #MARKDOWN_SUB
    def __sub__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
        if lhs.magnitude == WholeNumber(0):  # 0 - a = -a, why add this? it simplifies logic below because 0 has no sign
            new_sign = rhs.sign
            if new_sign == Sign.POSITIVE:
                new_sign = Sign.NEGATIVE
            elif new_sign == Sign.NEGATIVE:
                new_sign = Sign.POSITIVE
            return IntegerNumber(new_sign, rhs.magnitude)
        if rhs.magnitude == WholeNumber(0):  # a - 0 = a, why add this? it simplifies logic below because 0 has no sign
            return lhs.copy()

        if lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE:
            if lhs.magnitude >= rhs.magnitude:
                sign = Sign.POSITIVE
                magnitude = lhs.magnitude - rhs.magnitude
            elif lhs.magnitude < rhs.magnitude:
                sign = Sign.NEGATIVE
                magnitude = rhs.magnitude - lhs.magnitude
        elif lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE:
            if lhs.magnitude >= rhs.magnitude:
                sign = Sign.NEGATIVE
                magnitude = lhs.magnitude - rhs.magnitude
            elif lhs.magnitude < rhs.magnitude:
                sign = Sign.POSITIVE
                magnitude = rhs.magnitude - lhs.magnitude
        elif lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE:
            sign = Sign.POSITIVE
            magnitude = lhs.magnitude + rhs.magnitude
        elif lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE:
            sign = Sign.NEGATIVE
            magnitude = lhs.magnitude + rhs.magnitude

        if magnitude == WholeNumber(0):
            sign = None

        return IntegerNumber(sign, magnitude)
    #MARKDOWN_SUB

    #MARKDOWN_MUL
    def __mul__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
        if lhs.magnitude == WholeNumber(0):  # 0 * a = 0, why add this? it simplifies logic below because 0 has no sign
            return IntegerNumber.from_int(0)
        if rhs.magnitude == WholeNumber(0):  # a * 0 = 0, why add this? it simplifies logic below because 0 has no sign
            return IntegerNumber.from_int(0)

        if (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE):
            sign = Sign.POSITIVE
            magnitude = lhs.magnitude * rhs.magnitude
        elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE):
            sign = Sign.NEGATIVE
            magnitude = lhs.magnitude * rhs.magnitude

        if magnitude == WholeNumber(0):
            sign = None

        return IntegerNumber(sign, magnitude)
    #MARKDOWN_MUL

    #MARKDOWN_DIV
    def __truediv__(lhs: IntegerNumber, rhs: IntegerNumber) -> (IntegerNumber, IntegerNumber):
        if lhs.magnitude == WholeNumber(0):  # 0 / a = 0, why add this? it simplifies logic below because 0 has no sign
            return IntegerNumber.from_int(0)
        if rhs.magnitude == WholeNumber(0):  # a / 0 = err, why add this? it simplifies logic below because 0 is err
            raise Exception('Cannot divide by 0')

        if (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE):
            (magnitude, remainder) = lhs.magnitude / rhs.magnitude
            magnitude_sign = Sign.POSITIVE
            remainder_sign = Sign.POSITIVE
        elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE):
            (magnitude, remainder) = lhs.magnitude / rhs.magnitude
            magnitude_sign = Sign.NEGATIVE
            remainder_sign = Sign.NEGATIVE

        if magnitude == WholeNumber(0):
            magnitude_sign = None
        if remainder == WholeNumber(0):
            remainder_sign = None

        return IntegerNumber(magnitude_sign, magnitude), IntegerNumber(remainder_sign, remainder)
    #MARKDOWN_DIV

    def __eq__(self: IntegerNumber, other: IntegerNumber) -> bool:
        return self.sign == other.sign and self.magnitude == other.magnitude

    def __lt__(self: IntegerNumber, other: IntegerNumber) -> bool:
        self_sign = self.sign
        if self_sign is None:  # assume 0 is a positive -- it simplifies logic below
            self_sign = Sign.POSITIVE

        other_sign = other.sign
        if other_sign is None:  # assume 0 is a positive -- it simplifies logic below
            other_sign = Sign.POSITIVE

        if self_sign == Sign.POSITIVE and other_sign == Sign.POSITIVE:
            return self.magnitude < other.magnitude
        elif self_sign == Sign.NEGATIVE and other_sign == Sign.NEGATIVE:
            return self.magnitude > other.magnitude
        elif self_sign == Sign.POSITIVE and other_sign == Sign.NEGATIVE:
            return False
        elif self_sign == Sign.NEGATIVE and other_sign == Sign.POSITIVE:
            return True

    def __le__(self: IntegerNumber, other: IntegerNumber) -> bool:
        return self < other or self == other

    def __gt__(self: IntegerNumber, other: IntegerNumber) -> bool:
        self_sign = self.sign
        if self_sign is None:  # assume 0 is a positive -- it simplifies logic below
            self_sign = Sign.POSITIVE

        other_sign = other.sign
        if other_sign is None:  # assume 0 is a positive -- it simplifies logic below
            other_sign = Sign.POSITIVE

        if self_sign == Sign.POSITIVE and other_sign == Sign.POSITIVE:
            return self.magnitude > other.magnitude
        elif self_sign == Sign.NEGATIVE and other_sign == Sign.NEGATIVE:
            return self.magnitude < other.magnitude
        elif self_sign == Sign.POSITIVE and other_sign == Sign.NEGATIVE:
            return True
        elif self_sign == Sign.NEGATIVE and other_sign == Sign.POSITIVE:
            return False

    def __ge__(self: IntegerNumber, other: IntegerNumber) -> bool:
        return self > other or self == other

    def __str__(self: IntegerNumber) -> str:
        return ('-' if self.sign == Sign.NEGATIVE else '') + str(self.magnitude)


class Sign(Enum):
    POSITIVE = 1
    NEGATIVE = 2


if __name__ == '__main__':
    # mag, rem = IntegerNumber.from_int(-30) / IntegerNumber.from_int(-5)
    # print(f'{mag}R{rem}')

    # print(f'{IntegerNumber.from_int(30) * IntegerNumber.from_int(5)}')

    print(f'{IntegerNumber.from_int(0) == IntegerNumber.from_int(0)}')