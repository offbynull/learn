from __future__ import annotations

from typing import List, Union

from Digit import Digit
from Output import log_decorator, log, log_indent, log_unindent


class PartialNumber:

    @staticmethod
    def from_str(digits: str):
        digits = list(map(lambda i: Digit(int(i)), digits))
        digits.reverse()
        return PartialNumber(digits)

    @staticmethod
    def from_digit(digit: Digit):
        return PartialNumber.from_digit_list([digit])

    @staticmethod
    def from_digit_list(digits: List[Digit]):
        return PartialNumber(digits)

    @staticmethod
    def from_int_list(digits: List[int]):
        digits = list(map(lambda i: Digit(i), digits))
        return PartialNumber(digits)

    def __init__(self, digits: List[Digit]):
        if digits is None:
            self.digits = [Digit(0)]
        elif isinstance(digits, Digit):
            self.digits = [digits]
        elif isinstance(digits, list):
            self.digits = list(map(lambda i: Digit(i) if isinstance(i, int) else i, digits))
        elif isinstance(digits, str):
            self.digits = list(map(lambda i: Digit(int(i)), digits))
            self.digits.reverse()
        elif isinstance(digits, int):
            if digits < 0:
                raise Exception('Negative int not allowed')
            digits = str(digits)
            self.digits = list(map(lambda i: Digit(int(i)), digits))
            self.digits.reverse()
        else:
            raise Exception()

        self._prune_unnecessary_0s()

    def copy(self: PartialNumber) -> PartialNumber:
        return PartialNumber(self.digits)

    def __getitem__(self, key) -> Digit:
        if key >= len(self.digits):
            return Digit(0)
        return self.digits[len(self.digits) - key - 1]

    def __setitem__(self: PartialNumber, key: int, value: Union[Digit, int]) -> None:
        if key >= len(self.digits):
            excess = key - len(self.digits) + 1
            self.digits[0:0] = [Digit(0)] * excess  # insert at 0
        if isinstance(value, int):
            self.digits[len(self.digits) - key - 1] = Digit(value)
        elif isinstance(value, Digit):
            self.digits[len(self.digits) - key - 1] = value
        else:
            raise Exception()

        self._prune_unnecessary_0s()

    def __len__(self: PartialNumber) -> int:
        return len(self.digits)

    def __str__(self: PartialNumber) -> str:
        output = ''
        for digit in reversed(self.digits):
            output += str(digit.value)
        return output

    def __repr__(self: PartialNumber):
        return self.__str__()

    def __hash__(self):
        return hash(tuple(self.digits))

    def _prune_unnecessary_0s(self: PartialNumber) -> None:
        trim_count = 0
        for digit in self.digits:
            if digit == 0:
                trim_count += 1
            else:
                break

        self.digits = self.digits[trim_count:]

        # if empty, keep a single digit there
        if len(self.digits) == 0:
            self.digits = [Digit(0)]

    @log_decorator
    def __eq__(self: PartialNumber, other: PartialNumber) -> bool:
        if not isinstance(other, PartialNumber):
            raise Exception()

        log(f'Equality testing {self} and {other}...')
        log_indent()

        ret = self.digits == other.digits

        log_unindent()
        log(f'{ret}')

        return ret

    @log_decorator
    def __lt__(self: PartialNumber, other: PartialNumber) -> bool:
        if not isinstance(other, PartialNumber):
            raise Exception()

        log(f'Less than testing {self} and {other}...')
        log_indent()

        count = max(len(self.digits), len(other.digits))
        for pos in range(0, count):  # from smallest to largest component
            log(f'Test digits {self[pos]} and {other[pos]}...')
            if self[pos] > other[pos]:
                log(f'{self[pos]} > {other[pos]} -- {self} is NOT less than {other}, it is greater than')
                return False
            elif self[pos] < other[pos]:
                log(f'{self[pos]} < {other[pos]} -- {self} is less than {other}')
                return True
            else:
                log(f'{self[pos]} == {other[pos]} -- continuing testing')

        log(f'No more digits to test -- {self} is NOT less than {other}, it is equal')
        return False

    @log_decorator
    def __gt__(self: PartialNumber, other: PartialNumber) -> bool:
        if not isinstance(other, PartialNumber):
            raise Exception()

        log(f'Greater than testing {self} and {other}...')
        log_indent()

        count = max(len(self.digits), len(other.digits))
        for pos in range(0, count):  # from smallest to largest component
            log(f'Test digits {self[pos]} and {other[pos]}...')
            if self[pos] > other[pos]:
                log(f'{self[pos]} > {other[pos]} -- {self} is greater than {other}')
                return True
            elif self[pos] < other[pos]:
                log(f'{self[pos]} < {other[pos]} -- {self} is NOT greater than {other}, it is less than')
                return False
            else:
                log(f'{self[pos]} == {other[pos]} -- continuing testing')

        log(f'No more digits to test -- {self} is NOT greater than {other}, it is equal')
        return False


if __name__ == '__main__':
    print(f'{PartialNumber.from_str("401") < PartialNumber.from_str("45")}')
    print(f'{PartialNumber.from_str("45") < PartialNumber.from_str("401")}')

    print(f'{PartialNumber.from_str("401") > PartialNumber.from_str("45")}')
    print(f'{PartialNumber.from_str("45") > PartialNumber.from_str("401")}')

    print(f'{PartialNumber.from_str("400") == PartialNumber.from_str("4")}')
    print(f'{PartialNumber.from_str("4") == PartialNumber.from_str("400")}')
    print(f'{PartialNumber.from_str("4") == PartialNumber.from_str("401")}')

    # print(f'{PartialNumber.from_str("4")}')
    # print(f'{PartialNumber.from_str("04")}')
    # print(f'{PartialNumber.from_str("040")}')
    # print(f'{PartialNumber.from_str("140")}')
    # print(f'{PartialNumber.from_str("140")[0]}')
    # print(f'{PartialNumber.from_str("140")[1]}')
    # print(f'{PartialNumber.from_str("140")[2]}')
    #
    # test = PartialNumber.from_str("140")
    # print(f'{test}')
    # test[0] = Digit(9)
    # print(f'{test}')
    # test[1] = Digit(8)
    # print(f'{test}')
    # test[4] = Digit(5)
    # print(f'{test}')