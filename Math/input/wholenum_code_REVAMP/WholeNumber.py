from __future__ import annotations
from typing import Union, List

from Digit import Digit


indent_offset = -2
first_line = True
disableCounter = 0

def output_disable():
    global disableCounter
    disableCounter += 1

def output_enable():
    global disableCounter
    disableCounter -= 1

def output_indent():
    global indent_offset, first_line
    indent_offset += 2
    first_line = True

def output_unindent():
    global indent_offset, first_line
    indent_offset -= 2

def output(data):
    global indent_offset, first_line, disableCounter

    if disableCounter > 0:
        return

    data = (' ' * indent_offset) + ' * ' + data
    print(data)


class WholeNumber:
    def __init__(self, digits: Union[List[Digit], str, int, Digit, None] = None):
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
            digits = str(digits)
            self.digits = list(map(lambda i: Digit(int(i)), digits))
            self.digits.reverse()
        else:
            raise Exception()

        self._prune_unnecessary_0s()

    def __getitem__(self, key) -> Digit:
        if key >= len(self.digits):
            return Digit(0)
        return self.digits[key]

    def __setitem__(self: WholeNumber, key: int, value: Union[Digit, int]) -> None:
        if key >= len(self.digits):
            excess = key - len(self.digits) + 1
            self.digits.extend([Digit(0)] * excess)
        if isinstance(value, int):
            self.digits[key] = Digit(value)
        elif isinstance(value, Digit):
            self.digits[key] = value
        else:
            raise Exception()

        self._prune_unnecessary_0s()

    def __len__(self: WholeNumber) -> int:
        return len(self.digits)

    def __str__(self: WholeNumber) -> str:
        output = ''
        for digit in reversed(self.digits):
            output += str(digit.value)
        return output

    def _as_int(self: WholeNumber) -> int:
        return int(str(self))

    def _as_digit(self: WholeNumber) -> Digit:
        return Digit(int(str(self)), allowOob=True)

    def _highlight(self: WholeNumber, *idxes: int) -> None:
        digits_copy = self.digits[:]

        max_idxes = max(idxes)
        if max_idxes >= len(digits_copy):
            excess = max_idxes - len(digits_copy) + 1
            digits_copy.extend([Digit(0)] * excess)

        output_str = ''
        for i in range(0, len(digits_copy)):
            dout = str(digits_copy[i].value)
            output_str = ('[' + dout + ']' if i in idxes else dout) + ' ' + output_str
        return output_str

    def shift_left(self: WholeNumber, count: int) -> None:
        for i in range(0, count):
            self.digits.insert(0, Digit(0))

    def _prune_unnecessary_0s(self: WholeNumber) -> None:
        trim_count = 0
        for digit in reversed(self.digits):
            if digit == 0:
                trim_count += 1
            else:
                break

        self.digits = self.digits[:len(self.digits) - trim_count]

        # if empty, keep a single digit there
        if len(self.digits) == 0:
            self.digits = [Digit(0)]

    def copy(self: WholeNumber) -> WholeNumber:
        return WholeNumber(self.digits)



    def __eq__(self: WholeNumber, other: WholeNumber) -> bool:
        if isinstance(other, int):
            other = WholeNumber(other)
        elif isinstance(other, str):
            other = WholeNumber(other)

        if not isinstance(other, WholeNumber):
            raise Exception()

        return self.digits == other.digits

    def __lt__(self: WholeNumber, other: WholeNumber) -> bool:
        if isinstance(other, int):
            other = WholeNumber(other)
        elif isinstance(other, str):
            other = WholeNumber(other)

        if not isinstance(other, WholeNumber):
            raise Exception()

        count = max(len(self.digits), len(other.digits))
        for pos in reversed(range(0, count)):  # from smallest to largest component
            if self[pos] > other[pos]:
                return False
            elif self[pos] < other[pos]:
                return True
            else:
                pass
        return False

    def __le__(self: WholeNumber, other: WholeNumber) -> bool:
        return self < other or self == other

    def __gt__(self: WholeNumber, other: WholeNumber) -> bool:
        if isinstance(other, int):
            other = WholeNumber(other)
        elif isinstance(other, str):
            other = WholeNumber(other)

        if not isinstance(other, WholeNumber):
            raise Exception()

        count = max(len(self.digits), len(other.digits))
        for pos in reversed(range(0, count)):  # from smallest to largest component
            if self[pos] > other[pos]:
                return True
            elif self[pos] < other[pos]:
                return False
            else:
                pass
        return False

    def __ge__(self: WholeNumber, other: WholeNumber) -> bool:
        return self > other or self == other

    #MARKDOWN_ADD
    def __add__(self: WholeNumber, other: WholeNumber) -> WholeNumber:
        output_indent()
        try:
            cache = [
                [0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
                [1,  2,  3,  4,  5,  6,  7,  8,  9, 10],
                [2,  3,  4,  5,  6,  7,  8,  9, 10, 11],
                [3,  4,  5,  6,  7,  8,  9, 10, 11, 12],
                [4,  5,  6,  7,  8,  9, 10, 11, 12, 13],
                [5,  6,  7,  8,  9, 10, 11, 12, 13, 14],
                [6,  7,  8,  9, 10, 11, 12, 13, 14, 15],
                [7,  8,  9, 10, 11, 12, 13, 14, 15, 16],
                [8,  9, 10, 11, 12, 13, 14, 15, 16, 17],
                [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
            ]

            count = max(len(self.digits), len(other.digits))

            carryover_digit = None
            result = WholeNumber()
            for pos in range(0, count):  # from smallest to largest component
                output(f'Targeting {self._highlight(pos)} and {other._highlight(pos)}')
                output_indent()

                digit1 = self[pos]
                digit2 = other[pos]

                added = WholeNumber(cache[digit1.value][digit2.value])
                output(f'Using cache for initial add: {digit1} + {digit2} = {added}')

                if carryover_digit is not None:
                    output(f'Using recursion for carryover add: {added} + {carryover_digit} = ...')
                    added = added + WholeNumber(carryover_digit)  # recurse -- this called __add__()
                    carryover_digit = None

                if len(added) == 1:
                    result[pos] = added[0]
                elif len(added) == 2:
                    result[pos] = added[0]      # keep 1s digit
                    carryover_digit = added[1]  # carryover 10s digit
                else:
                    raise Exception('This should never happen')

                output(f'Result: {result._highlight(pos)}, Carryover: {carryover_digit}')
                output_unindent()

            if carryover_digit is not None:
                output(f'Remaining carryover: {self._highlight(count)}  [{carryover_digit}]')
                result[count] = carryover_digit
                output(f'Result: {result._highlight(count)}')

            return result
        finally:
            output_unindent()
    #MARKDOWN_ADD

    #MARKDOWN_SUB
    def __sub__(self: WholeNumber, other: WholeNumber) -> WholeNumber:
        output_indent()
        try:
            sub_cache = [
                [0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None],
                [7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None],
                [8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None],
                [9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None],
                [10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None],
                [11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None],
                [12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None],
                [13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None],
                [14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None],
                [15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None],
                [16,   15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None],
                [17,   16,   15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None],
                [18,   17,   16,   15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None],
                [19,   18,   17,   16,   15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0   ]
            ]

            # copy self because it may get modified during borrowing phase
            self_copy = self.copy()

            count = max(len(self_copy.digits), len(other.digits))

            result = WholeNumber()
            for pos in range(0, count):  # from smallest to largest component
                output(f'Targeting {self_copy._highlight(pos)} and {other._highlight(pos)}')
                output_indent()

                digit1 = self_copy[pos]
                digit2 = other[pos]
                result_digit = sub_cache[digit1.value][digit2.value]
                if result_digit is not None:
                    output(f'Using cache for subtraction: {digit1} - {digit2} = {result_digit}')
                else:
                    output('Not possible -- attempting to borrow')
                    self_copy._borrow_from_next(sub_cache, pos)

                    digit1 = self_copy[pos]
                    digit2 = other[pos]
                    result_digit = sub_cache[digit1.value][digit2.value]
                    output(f'Using cache for subtraction: {digit1} - {digit2} = {result_digit}')

                result[pos] = result_digit
                output(f'Result: {result._highlight(pos)}')
                output_unindent()

            return result
        finally:
            output_unindent()

    def _borrow_from_next(self: WholeNumber, sub_cache: List[List[int]], pos: int) -> None:
        output_indent()
        try:
            if pos >= len(self):
                raise Exception('Not enough available to borrow')

            curr_digit = self[pos]
            next_digit = self[pos + 1]

            output(f'Borrowing from next largest {self._highlight(pos + 1)}')

            if next_digit == 0:
                output(f'Not possible -- attempting to borrow again')
                self._borrow_from_next(sub_cache, pos + 1)  # recursively borrow
                next_digit = self[pos + 1]  # updated because of borrow call above

            next_digit = sub_cache[next_digit.value][1]                             # sub 1 from next largest position
            curr_digit = (WholeNumber(10) + WholeNumber(curr_digit))._as_digit()    # add 10 to current position

            # curr_digit is no longer an actual digit -- it's beyond the value of 9 (a digit is 0..9). We're using a
            # hack to get a out-of-bounds value as a digit because we need to subtract from it later on -- this is
            # trying to faithfully replicate the 'borrowing' logic in vertical subtraction

            self[pos + 1] = next_digit
            self[pos] = curr_digit

            output(f'Completed borrowing {self._highlight(pos, pos + 1)}')
        finally:
            output_unindent()
    #MARKDOWN_SUB

    #MARKDOWN_MUL
    def __mul__(self: WholeNumber, other: WholeNumber) -> WholeNumber:
        output_indent()
        try:
            count = len(other.digits)

            res_list = []
            for pos in range(0, count):  # from smallest to largest component
                output(f'Targeting {self} and {other._highlight(pos)}')
                output_indent()

                self_copy = self.copy()    # create a copy
                self_copy.shift_left(pos)  # shift copy (add 0s) based on the digit we're on
                output(f'Appending 0s to multiplicand based on position of multiplier (pos {pos}): {self_copy} {other._highlight(pos)}')

                res = self_copy._single_digit_mul(other[pos])  # multiply copy by that digit
                output_unindent()

                res_list.append(res)

            output(f'Summing intermediate results to get final result...')
            output_indent()
            final_res = WholeNumber()
            for res in res_list:
                output(f'Adding {res} to {final_res}')
                final_res += res
            output_unindent()

            output(f'Result: {final_res}')

            return final_res
        finally:
            output_unindent()

    def _single_digit_mul(self: WholeNumber, digit: Digit) -> WholeNumber:
        output_indent()
        try:
            cache = [
                [0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
                [0,  1,  2,  3,  4,  5,  6,  7,  8,  9 ],
                [0,  2,  4,  6,  8,  10, 12, 14, 16, 18],
                [0,  3,  6,  9,  12, 15, 18, 21, 24, 27],
                [0,  4,  8,  12, 16, 20, 24, 28, 32, 36],
                [0,  5,  10, 15, 20, 25, 30, 35, 40, 45],
                [0,  6,  12, 18, 24, 30, 36, 42, 48, 54],
                [0,  7,  14, 21, 28, 35, 42, 49, 56, 63],
                [0,  8,  16, 24, 32, 40, 48, 56, 64, 72],
                [0,  9,  18, 27, 36, 45, 54, 63, 72, 81]
            ]

            count = len(self.digits)

            carryover_digit = None
            result = WholeNumber()
            for pos in range(0, count):  # from smallest to largest component
                output(f'Targeting {self._highlight(pos)} and {digit}')
                output_indent()

                digit1 = self[pos]

                multed = WholeNumber(cache[digit1.value][digit.value])
                output(f'Using cache for initial mul: {digit1} * {digit} = {multed}')

                if carryover_digit is not None:
                    adjusted_multed = multed + WholeNumber(carryover_digit)
                    output(f'Adding carryover: {multed} + {carryover_digit} = {adjusted_multed}')
                    carryover_digit = None
                    multed = adjusted_multed

                if len(multed) == 1:
                    result[pos] = multed[0]
                elif len(multed) == 2:
                    result[pos] = multed[0]      # keep 1s digit
                    carryover_digit = multed[1]  # carryover 10s digit
                else:
                    raise Exception('This should never happen')

                output(f'Result: {result._highlight(pos)}, Carryover: {carryover_digit}')
                output_unindent()

            if carryover_digit is not None:
                output(f'Remaining carryover: {self._highlight(count)}  [{carryover_digit}]')
                result[count] = carryover_digit
                output(f'Result: {result._highlight(count)}')

            return result
        finally:
            output_unindent()
    #MARKDOWN_MUL

    #MARKDOWN_DIVTE
    @staticmethod
    def trial_and_error_div(dividend: WholeNumber, divisor: WholeNumber) -> (WholeNumber, WholeNumber):
        output_indent()
        try:
            output(f'Performing {dividend} / {divisor} ...')

            if dividend == 0:
                output(f'Found: {dividend} / {divisor} = 0R0')
                return WholeNumber(0)

            wn_range = WholeNumber.pick_start_range(dividend)
            output(f'START RANGE: [{wn_range.min}, {wn_range.max}]')

            quotient = None
            remainder = None
            while True:
                min_test = divisor * wn_range.min
                max_test = divisor * wn_range.max

                output(f'{divisor} * [{wn_range.min}, {wn_range.max}] = [{min_test}, {max_test}]')

                # check if found
                if min_test == dividend:  # found as min
                    quotient = wn_range.min
                    remainder = 0
                    break

                if max_test == dividend:  # found as max
                    quotient = wn_range.max
                    remainder = 0
                    break

                if min_test < dividend < max_test and wn_range.max - wn_range.min == 1:  # found between min and max
                    quotient = wn_range.min
                    remainder = dividend - min_test
                    break

                # not found, so modify range
                if min_test < dividend < max_test:
                    WholeNumber.narrow_range(dividend, divisor, wn_range)
                    output(f'NARROWING RANGE: [{wn_range.min}, {wn_range.max}]')
                elif min_test < dividend and max_test < dividend:
                    WholeNumber.move_up_range(wn_range)
                    output(f'INCREASING RANGE: [{wn_range.min}, {wn_range.max}]')
                elif min_test > dividend and max_test > dividend:
                    WholeNumber.move_down_range(wn_range)
                    output(f'DECREASING RANGE: [{wn_range.min}, {wn_range.max}]')

            return quotient, remainder
        finally:
            output_unindent()

    #MARKDOWN_DIVTE

    @staticmethod
    def pick_start_range(dividend: WholeNumber) -> WholeNumberRange:
        return WholeNumberRange(
            WholeNumber('1' + '0' * (len(dividend) - 1)),
            WholeNumber('1' + '0' * len(dividend))
        )

    @staticmethod
    def narrow_range(dividend: WholeNumber, divisor: WholeNumber, wn_range: WholeNumberRange) -> None:
        diff = wn_range.max - wn_range.min - WholeNumber(1)
        adjustment = WholeNumber('1' + ('0' * (len(diff) - 1)))

        min_test = divisor * wn_range.min
        max_test = divisor * wn_range.max

        if dividend - min_test > max_test - dividend:
            wn_range.min += adjustment
        else:
            wn_range.max -= adjustment

    @staticmethod
    def move_up_range(wn_range: WholeNumberRange) -> None:
        diff = wn_range.max - wn_range.min - WholeNumber(1)
        adjustment = WholeNumber('1' + ('0' * (len(diff) - 1)))

        wn_range.min += adjustment
        wn_range.max += adjustment

    @staticmethod
    def move_down_range(wn_range: WholeNumberRange) -> None:
        diff = wn_range.max - wn_range.min - WholeNumber(1)
        adjustment = WholeNumber('1' + ('0' * (len(diff) - 1)))

        wn_range.min -= adjustment
        wn_range.max -= adjustment


class WholeNumberRange:
    def __init__(self, min: WholeNumber, max: WholeNumber):
        self.min = min
        self.max = max

        if min > max:
            raise Exception()


if __name__ == '__main__':
    # n3 = WholeNumber('1000') - WholeNumber('100')
    # print(n3)
    (q, r) = WholeNumber.trial_and_error_div(WholeNumber(98), WholeNumber(3))
    print(f'{q}R{r}')
