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
        values = val.split('.')
        if len(values) == 1 and len(values[0]) > 0:
            wholes = FractionNumber.from_integer(
                IntegerNumber.from_str(values[0])
            )
            return DecimalNumber(wholes)
        elif len(values) == 2:
            wholes = FractionNumber(
                IntegerNumber.from_str(values[0]),
                IntegerNumber.from_str('1')
            )
            partial = FractionNumber(
                IntegerNumber.from_whole(
                    WholeNumber.from_str(values[1])
                ),
                IntegerNumber.from_whole(
                    WholeNumber.from_str('1' + ('0' * len(values[1])))
                )
            )
            return DecimalNumber(wholes + partial)
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

        log_unindent()

        ret = DecimalNumber(value)
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

    def __init__(self, value: FractionNumber):
        num = value.numerator
        denom = value.denominator
        if not str(denom).startswith('1'):
            raise Exception('Denominator must be power of 10')
        elif not set(str(denom)[1:]) == set('0') and not set(str(denom)[1:]) == set():
            raise Exception('Denominator must be power of 10')

        self.value = value

        num_digits_in_num = len(str(num))
        num_0s_in_den = len(str(denom)[1:])
        prepend_0s_to_num = num_0s_in_den - num_digits_in_num

        wholes, remaining = num / denom
        self.cached_wholes_str = str(wholes)
        self.cached_partial_str = '0' * prepend_0s_to_num + str(remaining)

    def __str__(self):
        if self.value.sign == Sign.POSITIVE:
            ret = '+'
        elif self.value.sign == Sign.NEGATIVE:
            ret = '-'
        else:
            ret = ''

        ret += self.cached_wholes_str + '.' + self.cached_partial_str

        return ret

    def __repr__(self: WholeNumber):
        return self.__str__()

    def __hash__(self):
        return hash(tuple([self.value]))

    #MARKDOWN_AS_FRAC
    @log_decorator
    def as_fraction(self) -> FractionNumber:
        log(f'Converting {self} to fraction number...')
        log_indent()

        log(f'Determining denominator based on length of partial portion ({self.cached_partial_str})...')
        denom = WholeNumber.from_str('1' + '0' * len(self.cached_partial_str))
        log(f'{denom}')

        log(f'Determining numerator based on denominator ({denom})...')
        num = WholeNumber.from_str(self.cached_wholes_str) * denom + WholeNumber.from_str(self.cached_partial_str)
        log(f'{num}')

        ret = FractionNumber(
            IntegerNumber(self.value.sign, num),
            IntegerNumber(Sign.POSITIVE, denom))

        log_unindent()

        log(f'{ret}')
        return ret
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

        output = ''
        if self.value.sign == Sign.NEGATIVE:
            output += 'negative '

        wholes = WholeNumber.from_str(self.cached_wholes_str)
        partials = WholeNumber.from_str(self.cached_partial_str)

        log(f'Converting wholes portion to words...')
        wholes_words = wholes.to_words()
        log(f'Wholes as words: {wholes_words}')

        log(f'Converting partial portion to words...')
        partial_words = partials.to_words()
        log(f'Partial as words: {partial_words}')

        if wholes != WholeNumber.from_str('0'):
            output = wholes_words

        if wholes != WholeNumber.from_str('0') and partials != WholeNumber.from_str('0'):
            output += ' and '

        if partials != WholeNumber.from_str('0'):
            output += partial_words
            suffix = partials_len_to_suffixes[len(self.cached_partial_str)]
            if suffix is None:
                raise Exception('Partial too large')
            log(f'Partial suffix: {suffix}')
            if partials > WholeNumber.from_str('1'):  # pluralize suffix if more than 1
                suffix += 's'
            output += ' ' + suffix

        log_unindent()
        log(f'{output}')

        return output.strip()
    #MARKDOWN_TO_WORDS


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

    print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-10/200")).to_words()}')
