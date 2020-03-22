from __future__ import annotations

from typing import Union, List, Set

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

    #MARKDOWN_ADD
    def __add__(lhs: FractionNumber, rhs: FractionNumber) -> FractionNumber:
        # Sign is only kept on the numerator, not the denominator
        log_indent()
        try:
            log(f'Adding {lhs} and {rhs}')
            if lhs._denominator != rhs._denominator:
                lhs_numerator = lhs._numerator * rhs._denominator
                rhs_numerator = rhs._numerator * lhs._denominator
                denominator = rhs._denominator * lhs._denominator
            else:
                lhs_numerator = lhs._numerator
                rhs_numerator = rhs._numerator
                denominator = rhs._denominator

            res = FractionNumber(lhs_numerator + rhs_numerator, denominator)
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
            log(f'Subtracting {lhs} and {rhs}')
            if lhs._denominator != rhs._denominator:
                lhs_numerator = lhs._numerator * rhs._denominator
                rhs_numerator = rhs._numerator * lhs._denominator
                denominator = rhs._denominator * lhs._denominator
            else:
                lhs_numerator = lhs._numerator
                rhs_numerator = rhs._numerator
                denominator = rhs._denominator

            res = FractionNumber(lhs_numerator - rhs_numerator, denominator)
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

    def simplify(self: FractionNumber) -> FractionNumber:
        # Sign is on the numerator
        log_indent()
        try:
            log(f'Simplifying {self}')

            numerator_factors = FractionNumber._calculate_factors(self._numerator.magnitude)
            log(f'Numerator factors: {numerator_factors}')
            denominator_factors = FractionNumber._calculate_factors(self._denominator.magnitude)
            log(f'Denominator factors: {numerator_factors}')

            common_factors = [f for f in denominator_factors if f in numerator_factors] # intersection of values
            log(f'Common factors: {common_factors}')
            largest_common_factor = max(common_factors)
            log(f'Largest common factors: {common_factors}')

            largest_common_factor_as_intnum = IntegerNumber(Sign.POSITIVE, largest_common_factor)
            divided_numerator, _ = self._numerator / largest_common_factor_as_intnum
            divided_denominator, _ = self._denominator / largest_common_factor_as_intnum

            res = FractionNumber(divided_numerator, divided_denominator)
            log(f'Divide both numerator and denominator by largest common factor to get result: {res}')

            return res
        finally:
            log_unindent()

    @staticmethod
    def _calculate_factors(test_num: WholeNumber) -> List[WholeNumber]:
        factors: List[WholeNumber] = []

        factor1 = WholeNumber(1)
        while factor1 <= test_num:
            (factor2, remainder) = test_num / factor1
            div_had_remainder = remainder > WholeNumber(0)
            if not div_had_remainder:
                factors.append(factor1)
                factors.append(factor2)

            if factor2 <= factor1:
                break

            factor1 += WholeNumber(1)

        return factors

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
