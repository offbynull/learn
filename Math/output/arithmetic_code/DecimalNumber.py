from __future__ import annotations

from Factor import factor_tree
from FractionNumber import FractionNumber
from IntegerNumber import IntegerNumber
from Output import log, log_indent, log_unindent, log_decorator
from Sign import Sign
from WholeNumber import WholeNumber


class DecimalNumber:

    @staticmethod
    def from_str(val: str) -> DecimalNumber:
        if val.startswith('-'):
            sign = Sign.NEGATIVE
        else:
            sign = Sign.POSITIVE

        values = val[1:].split('.')
        if len(values) == 1 and len(values[0]) > 0:
            return DecimalNumber(sign, values[0], '0')
        if len(values) == 2:
            return DecimalNumber(sign, values[0], values[1])
        else:
            raise Exception(f'Bad format: {val}')

    #MARKDOWN_TO_SUITABLE_FRAC
    @staticmethod
    @log_decorator
    def to_suitable_fraction(value: FractionNumber) -> FractionNumber:
        log(f'Converting {value} to an equivalent fraction with denominator that is power of 10...')
        log_indent()

        denom = value.denominator

        if str(denom)[0] == '1' and set(str(denom)[1:]) == {'0'}:
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
            value = value * FractionNumber.from_whole(scale_by, scale_by)
            log(f'{value}')

        log_unindent()
        log(f'{value}')

        return value
    #MARKDOWN_TO_SUITABLE_FRAC

    #MARKDOWN_FROM_FRAC
    @staticmethod
    @log_decorator
    def from_fraction(value: FractionNumber) -> DecimalNumber:
        log(f'Converting {value} to a decimal number...')
        log_indent()

        log(f'Converting {value} to suitable fraction...')
        value = DecimalNumber.to_suitable_fraction(value)
        log(f'{value}')

        log(f'Converting {value} to mixed number...')
        sign = value.sign
        wholes, _ = value.numerator / value.denominator
        fraction = FractionNumber.from_whole(
            value.numerator - (value.denominator * wholes),
            value.denominator)
        log(f'{sign} {wholes} {fraction}')

        log(f'Prepending 0s on to {value.numerator} (numer) based on 0 count in {value.denominator} (denom)...')
        num_digits_in_num = len(str(fraction.numerator))
        num_0s_in_den = len(str(fraction.denominator)[1:])
        prepend_0s_to_num =  num_0s_in_den - num_digits_in_num

        wholes_str = str(wholes)
        partial_str = '0' * prepend_0s_to_num + str(fraction.numerator)

        log_unindent()

        ret = DecimalNumber(sign, wholes_str, partial_str)
        log(f'Decimal number: {ret}')
        return ret
    #MARKDOWN_FROM_FRAC

    def __init__(self, sign: Sign, wholes: str, partial: str):
        self.sign = sign
        self.wholes = wholes.lstrip('0')
        self.partial = partial.rstrip('0')

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
        denom = WholeNumber.from_str('1' + '0' * len(self.partial))
        log(f'{denom}')

        log(f'Determining numerator based on denominator ({denom})...')
        num = WholeNumber.from_str(self.wholes) * denom + WholeNumber.from_str(self.partial)
        log(f'{num}')

        ret = FractionNumber(
            IntegerNumber(self.sign, num),
            IntegerNumber(Sign.POSITIVE, denom))

        log_unindent()

        log(f'{ret}')
        return ret
    #MARKDOWN_AS_FRAC


if __name__ == '__main__':
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

    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("5/10")).as_fraction()}')
    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-5/10")).as_fraction()}')
    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("15/10")).as_fraction()}')
    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-15/10")).as_fraction()}')

    print('---')

    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("1/2")).as_fraction()}')
    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/2")).as_fraction()}')
    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("3/2")).as_fraction()}')
    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-3/2")).as_fraction()}')

    print('---')

    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/20")).as_fraction()}')
    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-10/200")).as_fraction()}')
