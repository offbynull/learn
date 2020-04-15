from __future__ import annotations

from collections import Counter
from typing import Union, List, Set, Tuple

import Factor
from Factor import factor_tree
from GreatestCommonDivisor import gcd_euclid
from LeastCommonMultiple import lcm_prime_factorize
from Sign import Sign
from Output import log_indent, log_unindent, log
from IntegerNumber import IntegerNumber
from WholeNumber import WholeNumber


class FractionNumber:
    @staticmethod
    def from_int(numerator: int, denominator: int) -> FractionNumber:
        return FractionNumber(
            IntegerNumber.from_int(numerator),
            IntegerNumber.from_int(denominator)
        )

    @staticmethod
    def from_str(val: str) -> FractionNumber:
        inputs = val.split('/', 2)
        return FractionNumber(
            IntegerNumber.from_str(inputs[0].strip()),
            IntegerNumber.from_int(inputs[1].strip())
        )

    def __init__(self, numerator: IntegerNumber, denominator: IntegerNumber):
        if denominator == IntegerNumber.from_int(0):
            raise Exception('Denominator cannot be 0')

        self._numerator = numerator.copy()
        self._denominator = denominator.copy()
        self._normalize_sign()

    def _normalize_sign(self):
        # Normalize so that sign is on the numerator and the denominator is always positive
        if self._numerator.sign is None:  # sign of None means magnitude of 0
            self._numerator = IntegerNumber.from_int(0)
            self._denominator = IntegerNumber.from_int(1)
        elif self._numerator.sign != self._denominator.sign:
            self._numerator = IntegerNumber(Sign.NEGATIVE, self._numerator.magnitude)
            self._denominator = IntegerNumber(Sign.POSITIVE, self._denominator.magnitude)
        elif self._numerator.sign == self._numerator.sign:
            self._numerator = IntegerNumber(Sign.POSITIVE, self._numerator.magnitude)
            self._denominator = IntegerNumber(Sign.POSITIVE, self._denominator.magnitude)

    def copy(self: FractionNumber):
        return FractionNumber(self._numerator, self.denominator)

    @property
    def sign(self: FractionNumber) -> Union[Sign, None]:
        return self._numerator.sign

    @sign.setter
    def sign(self: FractionNumber, sign: Union[Sign, None]):
        self._numerator = IntegerNumber(sign, self._numerator.magnitude)
        self._normalize_sign()

    @property
    def numerator(self: FractionNumber) -> WholeNumber:
        return self._numerator.magnitude

    @numerator.setter
    def numerator(self: FractionNumber, numerator: WholeNumber):
        self._numerator = IntegerNumber(self._sign, numerator)
        self._normalize_sign()

    @property
    def denominator(self: FractionNumber) -> WholeNumber:
        return self._denominator.magnitude

    @denominator.setter
    def denominator(self: FractionNumber, denominator: WholeNumber):
        self._denominator = IntegerNumber(Sign.POSITIVE, denominator)
        self._normalize_sign()

    #MARKDOWN_COMMON_DENOMINATOR_NAIVE
    @staticmethod
    def common_denominator_naive(lhs: FractionNumber, rhs: FractionNumber) -> (FractionNumber, FractionNumber):
        # Sign is only kept on the numerator, not the denominator
        log_indent()
        try:
            log(f'Getting {lhs} and {rhs} to common denominator equivalent fractions')
            if lhs._denominator != rhs._denominator:
                log_indent()

                log(f'Calculating common denominator...')
                common_denominator = rhs._denominator * lhs._denominator
                log(f'{common_denominator}')

                log(f'Calculating numerator for LHS ({lhs})...')
                lhs_numerator = lhs._numerator * rhs._denominator
                log(f'{lhs_numerator}')

                log(f'Calculating numerator for RHS ({rhs})...')
                rhs_numerator = rhs._numerator * lhs._denominator
                log(f'{rhs_numerator}')

                log_unindent()

                lhs_equiv = FractionNumber(lhs_numerator, common_denominator)
                rhs_equiv = FractionNumber(rhs_numerator, common_denominator)
                log(f'Result: {lhs} -> {lhs_equiv}, {rhs} -> {rhs_equiv}')
                return lhs_equiv, rhs_equiv
            else:
                log(f'Fractions already have a common denominator')
                return lhs, rhs
        finally:
            log_unindent()
    #MARKDOWN_COMMON_DENOMINATOR_NAIVE

    #MARKDOWN_COMMON_DENOMINATOR_LCM
    @staticmethod
    def common_denominator_lcm(lhs: FractionNumber, rhs: FractionNumber) -> (FractionNumber, FractionNumber):
        # Sign is only kept on the numerator, not the denominator
        log_indent()
        try:
            log(f'Getting {lhs} and {rhs} to common denominator equivalent fractions')
            if lhs._denominator != rhs._denominator:
                log_indent()

                log(f'Calculating common denominator...')
                common_denominator = lcm_prime_factorize(rhs._denominator.magnitude, lhs._denominator.magnitude)
                common_denominator = IntegerNumber(Sign.POSITIVE, common_denominator)
                log(f'{common_denominator}')

                log(f'Calculating numerator for LHS ({lhs})...')
                multiple, _ = common_denominator / lhs._denominator
                lhs_numerator = lhs._numerator * multiple
                log(f'{lhs_numerator}')

                log(f'Calculating numerator for RHS ({rhs})...')
                multiple, _ = common_denominator / rhs._denominator
                rhs_numerator = rhs._numerator * multiple
                log(f'{rhs_numerator}')

                log_unindent()

                lhs_equiv = FractionNumber(lhs_numerator, common_denominator)
                rhs_equiv = FractionNumber(rhs_numerator, common_denominator)
                log(f'Result: {lhs} -> {lhs_equiv}, {rhs} -> {rhs_equiv}')
                return lhs_equiv, rhs_equiv
            else:
                log(f'Fractions already have a common denominator')
                return lhs, rhs
        finally:
            log_unindent()
    #MARKDOWN_COMMON_DENOMINATOR_LCM

    #MARKDOWN_ADD
    def __add__(lhs: FractionNumber, rhs: FractionNumber) -> FractionNumber:
        # Sign is only kept on the numerator, not the denominator
        log_indent()
        try:
            log(f'Adding {lhs} and {rhs}...')
            log_indent()

            log(f'Converting {lhs} and {rhs} to equivalent fractions with least common denominator...')
            lhs, rhs = FractionNumber.common_denominator_lcm(lhs, rhs)
            log(f'Equivalent fractions: {lhs} and {rhs}')
            log(f'Adding numerators of {lhs} and {rhs}...')
            res = FractionNumber(lhs._numerator + rhs._numerator, lhs._denominator)

            log_unindent()
            log(f'Result: {res}')

            return res
        finally:
            log_unindent()
    #MARKDOWN_ADD

    #MARKDOWN_SUB
    def __sub__(lhs: FractionNumber, rhs: FractionNumber) -> FractionNumber:
        # Sign is only kept on the numerator, not the denominator
        log_indent()
        try:
            log(f'Subtracting {lhs} and {rhs}...')
            log_indent()

            log(f'Converting {lhs} and {rhs} to equivalent fractions with least common denominator...')
            lhs, rhs = FractionNumber.common_denominator_lcm(lhs, rhs)
            log(f'Equivalent fractions: {lhs} and {rhs}')
            log(f'Subtracting numerators of {lhs} and {rhs}...')
            res = FractionNumber(lhs._numerator - rhs._numerator, lhs._denominator)

            log_unindent()
            log(f'Result: {res}')

            return res
        finally:
            log_unindent()
    #MARKDOWN_SUB

    #MARKDOWN_MUL
    def __mul__(lhs: FractionNumber, rhs: FractionNumber) -> FractionNumber:
        # Sign is only kept on the numerator, not the denominator
        log_indent()
        try:
            log(f'Multiplying {lhs} and {rhs}')

            res = FractionNumber(lhs._numerator * rhs._numerator, lhs._denominator * rhs._denominator)
            log(f'Result: {res}')

            return res
        finally:
            log_unindent()
    #MARKDOWN_MUL

    #MARKDOWN_DIV
    def __truediv__(lhs: FractionNumber, rhs: FractionNumber) -> FractionNumber:
        # Sign is only kept on the numerator, not the denominator
        log_indent()
        try:
            log(f'Dividing {lhs} and {rhs}')

            res = FractionNumber(lhs._numerator * rhs._denominator, lhs._denominator * rhs._numerator)
            log(f'Result: {res}')

            return res
        finally:
            log_unindent()
    #MARKDOWN_DIV

    #MARKDOWN_RECIP
    def reciprocal(self: FractionNumber) -> FractionNumber:
        # Sign is on the numerator
        log_indent()
        try:
            log(f'Getting reciprocal of {self}')

            res = FractionNumber(self._denominator, self._numerator)
            log(f'Result: {res}')

            return res
        finally:
            log_unindent()
    #NARKDOWN_RECIP

    #MARKDOWN_SIMP
    def simplify(self: FractionNumber) -> FractionNumber:
        log_indent()
        try:
            log(f'Simplifying {self}...')
            log_indent()

            log(f'Calculating GCD for ({self._numerator.magnitude}) and ({self._denominator.magnitude})...')
            gcd = gcd_euclid(self._numerator.magnitude, self._denominator.magnitude)
            log(f'GCD is {gcd}')

            log(f'Dividing numerator ({self._numerator.magnitude}) by {gcd}...')
            new_num, _ = self._numerator.magnitude / gcd
            log(f'New numerator is {new_num}...')

            log(f'Dividing denominator ({self._denominator.magnitude}) by {gcd}...')
            new_den, _ = self._denominator.magnitude / gcd
            log(f'New numerator is {new_den}...')

            # Sign of fraction is on the numerator
            if self.sign == Sign.NEGATIVE:  # if original was negative, so will the simplified
                res = FractionNumber(
                    IntegerNumber(Sign.NEGATIVE, new_num),
                    IntegerNumber(Sign.POSITIVE, new_den))
            else:  # if original was positive, so will the simplified
                res = FractionNumber(
                    IntegerNumber(Sign.POSITIVE, new_num),
                    IntegerNumber(Sign.POSITIVE, new_den))

            log_unindent()
            log(f'{self} simplified to: {res}')

            return res
        finally:
            log_unindent()
    #MARKDOWN_SIMP

    def __eq__(self: FractionNumber, other: FractionNumber) -> bool:
        # Sign is only kept on the numerator, not the denominator
        if self._denominator != other._denominator:
            lhs_numerator = self._numerator * other._denominator
            rhs_numerator = other._numerator * self._denominator
            denominator = other._denominator * self._denominator
        else:
            lhs_numerator = self._numerator
            rhs_numerator = other._numerator
            denominator = other._denominator

        return lhs_numerator == rhs_numerator

    def __lt__(self: FractionNumber, other: FractionNumber) -> bool:
        # Sign is only kept on the numerator, not the denominator
        if self._denominator != other._denominator:
            lhs_numerator = self._numerator * other._denominator
            rhs_numerator = other._numerator * self._denominator
            denominator = other._denominator * self._denominator
        else:
            lhs_numerator = self._numerator
            rhs_numerator = other._numerator
            denominator = other._denominator

        return lhs_numerator < rhs_numerator

    def __le__(self: FractionNumber, other: FractionNumber) -> bool:
        return self < other or self == other

    def __gt__(self: FractionNumber, other: FractionNumber) -> bool:
        # Sign is only kept on the numerator, not the denominator
        if self._denominator != other._denominator:
            lhs_numerator = self._numerator * other._denominator
            rhs_numerator = other._numerator * self._denominator
            denominator = other._denominator * self._denominator
        else:
            lhs_numerator = self._numerator
            rhs_numerator = other._numerator
            denominator = other._denominator

        return lhs_numerator > rhs_numerator

    def __ge__(self: FractionNumber, other: FractionNumber) -> bool:
        return self > other or self == other

    def __str__(self: FractionNumber) -> str:
        if self.sign == Sign.POSITIVE:
            sign_str = '+'
        elif self.sign == Sign.NEGATIVE:
            sign_str = '-'
        else:
            sign_str = ''
        return sign_str + str(self.numerator) + '/' + str(self.denominator)

    def __repr__(self: FractionNumber):
        return self.__str__()



if __name__ == '__main__':
    print(f'{FractionNumber.from_str("-3/5") + FractionNumber.from_str("1/5")} ')
    print(f'{FractionNumber.from_str("-1/5") + FractionNumber.from_str("3/5")} ')
    print(f'{FractionNumber.from_str("1/5") + FractionNumber.from_str("3/10")} ')
    print(f'{FractionNumber.from_str("1/5") * FractionNumber.from_str("3/10")} ')
    print(f'{FractionNumber.from_str("1/5") / FractionNumber.from_str("3/10")} ')

    print(f'{FractionNumber.from_str("2/5") == FractionNumber.from_str("4/10")}')
    print(f'{FractionNumber.from_str("2/5") != FractionNumber.from_str("4/10")}')
    print(f'{FractionNumber.from_str("1/5") > FractionNumber.from_str("3/10")}')
    print(f'{FractionNumber.from_str("2/5") > FractionNumber.from_str("3/10")}')
    print(f'{FractionNumber.from_str("1/5") < FractionNumber.from_str("3/10")}')
    print(f'{FractionNumber.from_str("2/5") < FractionNumber.from_str("3/10")}')

    print(f'{FractionNumber._calculate_factors(WholeNumber(55))}')

    print(f'{FractionNumber.from_str("3/12").simplify()}')
