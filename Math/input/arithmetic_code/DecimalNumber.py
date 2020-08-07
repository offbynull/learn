from __future__ import annotations

from typing import List, Union

from Digit import Digit
from Factor import factor_tree
from FractionNumber import FractionNumber
from IntegerNumber import IntegerNumber
from Output import log, log_indent, log_unindent, log_decorator
from PartialNumber import PartialNumber
from Sign import Sign
from WholeNumber import WholeNumber


class DecimalNumber:

    @staticmethod
    def from_str(val: str) -> DecimalNumber:
        values = val.split('.')
        if len(values) == 1 and len(values[0]) > 0:
            return DecimalNumber.from_integer(
                IntegerNumber.from_str(values[0])
            )
        elif len(values) == 2:
            if values[0][0] == '-':
                sign = Sign.NEGATIVE
                values[0] = values[0][1:]
            elif values[0][0] == '+':
                sign = Sign.POSITIVE
                values[0] = values[0][1:]
            elif values[0] == '0':
                sign = None
            else:
                sign = Sign.POSITIVE

            wholes = FractionNumber(
                IntegerNumber.from_whole(WholeNumber.from_str(values[0])),
                IntegerNumber.from_str('1')
            )
            partial = FractionNumber(
                IntegerNumber.from_whole(WholeNumber.from_str(values[1])),
                IntegerNumber.from_whole(WholeNumber.from_str('1' + ('0' * len(values[1]))))
            )

            final_frac = wholes + partial
            if sign == Sign.NEGATIVE:
                final_frac = final_frac * FractionNumber.from_str("-1/1")

            return DecimalNumber.from_fraction(final_frac)
        else:
            raise Exception(f'Bad format: {val}')

    @staticmethod
    def from_whole(value: WholeNumber):
        return DecimalNumber.from_fraction(FractionNumber.from_whole(value))

    @staticmethod
    def from_integer(value: IntegerNumber):
        return DecimalNumber.from_fraction(FractionNumber.from_integer(value))

    @staticmethod
    def from_int(value: int):
        return DecimalNumber.from_fraction(FractionNumber.from_int(value))

    #MARKDOWN_FROM_FRAC
    @staticmethod
    @log_decorator
    def from_fraction(value: FractionNumber) -> DecimalNumber:
        log(f'Converting {value} to a decimal number...')
        log_indent()

        log(f'Converting {value} to suitable fraction...')
        value = DecimalNumber.to_suitable_fraction(value)
        log(f'{value}')

        num = value.numerator
        denom = value.denominator
        if not str(denom).startswith('1'):
            raise Exception('Denominator must be power of 10')
        elif not set(str(denom)[1:]) == set('0') and not set(str(denom)[1:]) == set():
            raise Exception('Denominator must be power of 10')

        log(f'Resolving fraction {value}...')
        wholes, remaining = num / denom
        log(f'{wholes} wholes and {remaining} remaining')

        log(f'Converting {remaining} of {denom} to partial value...')
        num_digits_in_rem = len(remaining.digits)
        num_0s_in_den = len(denom.digits) - 1  # starts with 1 followed by 0s, so - 1 to ignore the starting 1
        num_0s_to_prepend_to_rem = num_0s_in_den - num_digits_in_rem
        partials_digits = remaining.digits[:]  # copy digits
        partials_digits = partials_digits + [Digit(0)] * num_0s_to_prepend_to_rem  # this prepending 0s...
                                                                                   # you might be confused because the
                                                                                   # 0s are being addeed to the end, but
                                                                                   # that's how PartialNumber expects
                                                                                   # digits -- in reversed order
        partials = PartialNumber(partials_digits)
        log(f'{partials}')

        sign = value.sign

        log_unindent()

        ret = DecimalNumber(sign, wholes, partials)
        log(f'Decimal number: {ret}')
        return ret
    #MARKDOWN_FROM_FRAC

    #MARKDOWN_TO_SUITABLE_FRAC
    @staticmethod
    @log_decorator
    def to_suitable_fraction(value: FractionNumber) -> FractionNumber:
        log(f'Converting {value} to an equivalent fraction with denominator that is power of 10...')
        log_indent()

        denom = value.denominator

        if str(denom)[0] == '1' and (set(str(denom)[1:]) == set() or set(str(denom)[1:]) == set('0')):
            log(f'Already power of 10')
        else:
            log(f'No')
            log(f'Simplifying fraction {value}...')
            value = value.simplify()
            denom = value.denominator
            log(f'{value}')

            log(f'Calculating unique prime factors of {denom}...')
            denom_prime_factors = factor_tree(denom).get_prime_factors()
            denom_prime_factors_set = set(denom_prime_factors)
            log(f'{denom_prime_factors_set}')
            if not({WholeNumber.from_int(2), WholeNumber.from_int(5)} == denom_prime_factors_set
                   or {WholeNumber.from_int(2)} == denom_prime_factors_set
                   or {WholeNumber.from_int(5)} == denom_prime_factors_set):
                raise Exception('Simplified denominator contains prime factors other than 2 and 5')

            log(f'Calculating value to scale by so {denom} becomes next largest power of 10...')
            expected_0s_in_denom = len(str(denom))
            expected_denom = WholeNumber.from_str('1' + '0' * expected_0s_in_denom)
            scale_by, _ = expected_denom / denom  # remainder will be 0
            log(f'{scale_by}')

            log(f'Scaling {value} by {scale_by}...')
            value = value * FractionNumber(
                IntegerNumber.from_whole(scale_by),
                IntegerNumber.from_whole(scale_by)
            )
            log(f'{value}')

        log_unindent()
        log(f'{value}')

        return value
    #MARKDOWN_TO_SUITABLE_FRAC

    def __init__(self, sign: Union[Sign, None], wholes: WholeNumber, partial: PartialNumber):
        self.sign = sign
        self.wholes = wholes.copy()
        self.partial = partial.copy()

        if wholes == WholeNumber.from_str('0') and partial == PartialNumber.from_str('0') and sign is not None:
            raise Exception('Magnitude of 0 cannot have a sign')

    def copy(self: DecimalNumber) -> DecimalNumber:
        return DecimalNumber(self.sign, self.wholes, self.partial)

    def __str__(self):
        if self.sign == Sign.POSITIVE:
            ret = '+'
        elif self.sign == Sign.NEGATIVE:
            ret = '-'
        else:
            ret = ''

        ret += str(self.wholes) + '.' + str(self.partial)

        return ret

    def __repr__(self: WholeNumber):
        return self.__str__()

    def __hash__(self):
        return hash(tuple([self.sign, self.wholes, self.partial]))

    #MARKDOWN_AS_FRAC
    @log_decorator
    def as_fraction(self) -> FractionNumber:
        log(f'Converting {self} to fraction number...')
        log_indent()

        log(f'Determining denominator based on length of partial portion ({self.partial})...')
        denom = IntegerNumber.from_str('1' + '0' * len(self.partial.digits))
        log(f'{denom}')

        log(f'Converting partial portion ({self.partial} to fraction...')
        partial_fraction = FractionNumber(
            IntegerNumber.from_str(str(self.partial)),
            denom
        )
        log(f'{partial_fraction}')

        log(f'Converting whole portion ({self.wholes}) to fraction...')
        wholes_fraction = FractionNumber.from_whole(self.wholes)
        log(f'{wholes_fraction}')

        log(f'Adding ({wholes_fraction}) to ({partial_fraction})...')
        fraction = wholes_fraction + partial_fraction
        log(f'{fraction}')

        log(f'Applying sign of ({self.sign}) to {fraction}...')
        if self.sign == Sign.NEGATIVE:
            fraction = fraction * FractionNumber.from_str("-1/1")  # make sign negative
        log(f'{fraction}')

        log_unindent()

        return fraction
    #MARKDOWN_AS_FRAC

    #MARKDOWN_TO_WORDS
    @log_decorator
    def to_words(self):
        partials_len_to_suffixes = {
            1: 'tenth',
            2: 'hundredth',
            3: 'thousandth',
            4: 'ten-thousandth',
            5: 'hundred-thousandth',
            6: 'millionth',
            7: 'ten-millionth',
            8: 'hundred-millionth',
            9: 'billionth',
            10: 'ten-billionth',
            11: 'hundred-billionth',
            12: 'trillionth',
            13: 'ten-trillionth',
            14: 'hundred-trillionth',
            15: 'quadrillionth',
            16: 'ten-quadrillionth',
            17: 'hundred-quadillionth',
            18: 'quintillionth',
            19: 'ten-quintillionth',
            20: 'hundred-quintillionth',
        }

        log(f'Converting {self}...')
        log_indent()

        log(f'Converting wholes portion to words...')
        wholes_words = self.wholes.to_words()
        log(f'Wholes as words: {wholes_words}')

        log(f'Converting partial portion to words...')
        partial_words = WholeNumber.from_str(str(self.partial)).to_words()
        log(f'Partial as words: {partial_words}')

        output = ''
        if self.wholes == WholeNumber.from_str('0') and self.partial == PartialNumber.from_str('0'):
            output += 'zero'
        else:
            if self.sign == Sign.NEGATIVE:
                output += 'negative '

            if self.wholes != WholeNumber.from_str('0'):
                output += wholes_words

            if self.wholes != WholeNumber.from_str('0') and self.partial != PartialNumber.from_str('0'):
                output += ' and '

            if self.partial != PartialNumber.from_str('0'):
                output += partial_words
                suffix = partials_len_to_suffixes[len(self.partial.digits)]
                if suffix is None:
                    raise Exception('Partial too large')
                log(f'Partial suffix: {suffix}')
                if self.partial != PartialNumber.from_str('0'):  # pluralize suffix if more than 1
                    suffix += 's'
                output += ' ' + suffix

        log_unindent()
        log(f'{output}')

        return output.strip()
    #MARKDOWN_TO_WORDS

    #MARKDOWN_EQ
    @log_decorator
    def __eq__(self: DecimalNumber, other: DecimalNumber) -> bool:
        log(f'Equality testing {self} and {other}...')
        log_indent()

        adjust_len = max(
            len(self.partial.digits),
            len(other.partial.digits)
        )

        log(f'Generating mock integer number for {self}...')
        self_extra_0s = adjust_len - len(self.partial.digits)
        self_combined_digits = self.partial.digits + self.wholes.digits
        self_combined_digits[0:0] = [Digit(0)] * self_extra_0s
        mock_self = IntegerNumber(self.sign, WholeNumber(self_combined_digits))
        log(f'{mock_self}')

        log(f'Generating mock integer number for {other}...')
        other_extra_0s = adjust_len - len(other.partial.digits)
        other_combined_digits = other.partial.digits + other.wholes.digits
        other_combined_digits[0:0] = [Digit(0)] * other_extra_0s
        mock_other = IntegerNumber(other.sign, WholeNumber(other_combined_digits))
        log(f'{mock_other}')

        log(f'Testing {mock_self} == {mock_other}...')
        ret = mock_self == mock_other
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_EQ

    #MARKDOWN_LT
    @log_decorator
    def __lt__(self: DecimalNumber, other: DecimalNumber) -> bool:
        log(f'Less than testing {self} and {other}...')
        log_indent()

        adjust_len = max(
            len(self.partial.digits),
            len(other.partial.digits)
        )

        log(f'Generating mock integer number for {self}...')
        self_extra_0s = adjust_len - len(self.partial.digits)
        self_combined_digits = self.partial.digits + self.wholes.digits
        self_combined_digits[0:0] = [Digit(0)] * self_extra_0s
        mock_self = IntegerNumber(self.sign, WholeNumber(self_combined_digits))
        log(f'{mock_self}')

        log(f'Generating mock integer number for {other}...')
        other_extra_0s = adjust_len - len(other.partial.digits)
        other_combined_digits = other.partial.digits + other.wholes.digits
        other_combined_digits[0:0] = [Digit(0)] * other_extra_0s
        mock_other = IntegerNumber(other.sign, WholeNumber(other_combined_digits))
        log(f'{mock_other}')

        log(f'Testing {mock_self} < {mock_other}...')
        ret = mock_self == mock_other
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_LT

    def __le__(self: DecimalNumber, other: DecimalNumber) -> bool:
        return self < other or self == other

    #MARKDOWN_GT
    @log_decorator
    def __gt__(self: DecimalNumber, other: DecimalNumber) -> bool:
        log(f'Greater than testing {self} and {other}...')
        log_indent()

        adjust_len = max(
            len(self.partial.digits),
            len(other.partial.digits)
        )

        log(f'Generating mock integer number for {self}...')
        self_extra_0s = adjust_len - len(self.partial.digits)
        self_combined_digits = self.partial.digits + self.wholes.digits
        self_combined_digits[0:0] = [Digit(0)] * self_extra_0s
        mock_self = IntegerNumber(self.sign, WholeNumber(self_combined_digits))
        log(f'{mock_self}')

        log(f'Generating mock integer number for {other}...')
        other_extra_0s = adjust_len - len(other.partial.digits)
        other_combined_digits = other.partial.digits + other.wholes.digits
        other_combined_digits[0:0] = [Digit(0)] * other_extra_0s
        mock_other = IntegerNumber(other.sign, WholeNumber(other_combined_digits))
        log(f'{mock_other}')

        log(f'Testing {mock_self} > {mock_other}...')
        ret = mock_self == mock_other
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_GT

    def __ge__(self: DecimalNumber, other: DecimalNumber) -> bool:
        return self > other or self == other

    #MARKDOWN_ADD
    @log_decorator
    def __add__(self: DecimalNumber, other: DecimalNumber) -> bool:
        log(f'Greater than testing {self} and {other}...')
        log_indent()

        adjust_len = max(
            len(self.partial.digits),
            len(other.partial.digits)
        )

        log(f'Generating mock integer number for {self}...')
        self_extra_0s = adjust_len - len(self.partial.digits)
        self_combined_digits = self.partial.digits + self.wholes.digits
        self_combined_digits[0:0] = [Digit(0)] * self_extra_0s
        mock_self = IntegerNumber(self.sign, WholeNumber(self_combined_digits))
        log(f'{mock_self}')

        log(f'Generating mock integer number for {other}...')
        other_extra_0s = adjust_len - len(other.partial.digits)
        other_combined_digits = other.partial.digits + other.wholes.digits
        other_combined_digits[0:0] = [Digit(0)] * other_extra_0s
        mock_other = IntegerNumber(other.sign, WholeNumber(other_combined_digits))
        log(f'{mock_other}')

        log(f'Performing {mock_self} + {mock_other}...')
        mock_ret = mock_self + mock_other
        log(f'{mock_ret}')

        log(f'Unmocking {mock_ret}...')
        ret_sign = mock_ret.sign
        ret_partial_digits = [mock_ret.magnitude[i] for i in range(0, adjust_len)]
        ret_whole_digits = [mock_ret.magnitude[i] for i in range(adjust_len, len(mock_ret.magnitude.digits))]
        ret = DecimalNumber(ret_sign, WholeNumber(ret_whole_digits), PartialNumber(ret_partial_digits))
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_ADD

    #MARKDOWN_SUB
    @log_decorator
    def __sub__(self: DecimalNumber, other: DecimalNumber) -> bool:
        log(f'Greater than testing {self} and {other}...')
        log_indent()

        adjust_len = max(
            len(self.partial.digits),
            len(other.partial.digits)
        )

        log(f'Generating mock integer number for {self}...')
        self_extra_0s = adjust_len - len(self.partial.digits)
        self_combined_digits = self.partial.digits + self.wholes.digits
        self_combined_digits[0:0] = [Digit(0)] * self_extra_0s
        mock_self = IntegerNumber(self.sign, WholeNumber(self_combined_digits))
        log(f'{mock_self}')

        log(f'Generating mock integer number for {other}...')
        other_extra_0s = adjust_len - len(other.partial.digits)
        other_combined_digits = other.partial.digits + other.wholes.digits
        other_combined_digits[0:0] = [Digit(0)] * other_extra_0s
        mock_other = IntegerNumber(other.sign, WholeNumber(other_combined_digits))
        log(f'{mock_other}')

        log(f'Performing {mock_self} + {mock_other}...')
        mock_ret = mock_self - mock_other
        log(f'{mock_ret}')

        log(f'Unmocking {mock_ret}...')
        ret_sign = mock_ret.sign
        ret_partial_digits = [mock_ret.magnitude[i] for i in range(0, adjust_len)]
        ret_whole_digits = [mock_ret.magnitude[i] for i in range(adjust_len, len(mock_ret.magnitude.digits))]
        ret = DecimalNumber(ret_sign, WholeNumber(ret_whole_digits), PartialNumber(ret_partial_digits))
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_SUB


if __name__ == '__main__':
    # print(f'{DecimalNumber.from_str("1.2").as_fraction()}')
    # print(f'{DecimalNumber.from_str("1.02").as_fraction()}')
    # print(f'{DecimalNumber.from_str("-1.20").as_fraction()}')
    # print(f'{DecimalNumber.from_str("-00.00").as_fraction()}')

    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("5/10"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-5/10"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("15/10"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-15/10"))}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("1/2"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/2"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("3/2"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-3/2"))}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/20"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-10/200"))}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/30"))}')  # this should fail

    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("5/10")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-5/10")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("15/10")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-15/10")).as_fraction()}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("1/2")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/2")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("3/2")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-3/2")).as_fraction()}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/20")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-10/200")).as_fraction()}')

    # print(f'{DecimalNumber.from_str("-1.2").to_words()}')
    # print(f'{DecimalNumber.from_str("-1.20").to_words()}')
    # print(f'{DecimalNumber.from_str("-1.02").to_words()}')
    # print(f'{DecimalNumber.from_str("0.1").to_words()}')
    # print(f'{DecimalNumber.from_str("-0.1").to_words()}')
    # print(f'{DecimalNumber.from_str("0.0").to_words()}')
    # print(f'{DecimalNumber.from_str("1.0").to_words()}')

    # print(f'{DecimalNumber.from_str("12.34") == DecimalNumber.from_str("012.340")}')
    # print(f'{DecimalNumber.from_str("12.34") == DecimalNumber.from_str("12.345")}')

    # print(f'{DecimalNumber.from_str("12.34") + DecimalNumber.from_str("12.34")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("0.02")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("0.2")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("-0.2")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("-0.02")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("-0.002")}')
    # print(f'{DecimalNumber.from_str("11.2") + DecimalNumber.from_str("-1.3")}')
    # print(f'{DecimalNumber.from_str("11.2") + DecimalNumber.from_str("1.3")}')
    # print(f'{DecimalNumber.from_str("0.0") + DecimalNumber.from_str("0.0")}')

    print(f'{DecimalNumber.from_str("12.34") - DecimalNumber.from_str("12.34")}')
    print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("0.02")}')
    print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("0.2")}')
    print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("-0.2")}')
    print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("-0.02")}')
    print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("-0.002")}')
    print(f'{DecimalNumber.from_str("11.2") - DecimalNumber.from_str("-1.3")}')
    print(f'{DecimalNumber.from_str("11.2") - DecimalNumber.from_str("1.3")}')
    print(f'{DecimalNumber.from_str("0.0") - DecimalNumber.from_str("0.0")}')
