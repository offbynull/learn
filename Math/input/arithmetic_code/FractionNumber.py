from __future__ import annotations

from typing import Union

import Sign
from Output import log_indent, log_unindent, log
from IntegerNumber import IntegerNumber
from WholeNumber import WholeNumber

class FractionNumber:
    def __init__(self, numerator: IntegerNumber, denominator: IntegerNumber):
        if denominator == IntegerNumber(0):
            raise Exception('Denominator cannot be 0')

        self.numerator = numerator.copy()
        self.denominator = denominator.copy()

        self._normalize_sign()

    def _normalize_sign(self):
        # Normalize so that sign is on the numerator and the denominator is always positive
        if self.numerator.sign is None:  # sign of None means magnitude of 0
            self.numerator = IntegerNumber(0)
            self.denominator = IntegerNumber(1)
        elif self.numerator.sign != self.denominator.sign:
            self.numerator = IntegerNumber(Sign.NEGATIVE, self.numerator.magnitude)
            self.denominator = IntegerNumber(Sign.POSITIVE, self.denominator.magnitude)
        elif self.numerator.sign == self.numerator.sign:
            self.numerator = IntegerNumber(Sign.POSITIVE, self.numerator.magnitude)
            self.denominator = IntegerNumber(Sign.POSITIVE, self.denominator.magnitude)

    def __add__(self: FractionNumber, other: FractionNumber) -> FractionNumber:
        if self.denominator != other.denominator:
            lhs_numerator = self.numerator * other.denominator
            rhs_numerator = other.numerator * self.denominator
            denominator = other.denominator * self.denominator
        else:
            lhs_numerator = self.numerator
            rhs_numerator = other.numerator
            denominator = other.denominator

        return FractionNumber(lhs_numerator + rhs_numerator, denominator)

    def __sub__(self: FractionNumber, other: FractionNumber) -> FractionNumber:
        if self.denominator != other.denominator:
            lhs_numerator = self.numerator * other.denominator
            rhs_numerator = other.numerator * self.denominator
            denominator = other.denominator * self.denominator
        else:
            lhs_numerator = self.numerator
            rhs_numerator = other.numerator
            denominator = other.denominator

        return FractionNumber(lhs_numerator - rhs_numerator, denominator)

    def __mul__(self: FractionNumber, other: FractionNumber) -> FractionNumber:
        return FractionNumber(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self: FractionNumber, other: FractionNumber) -> FractionNumber:
        return FractionNumber(self.numerator * other.denominator, self.denominator * other.numerator)

    def __str__(self: FractionNumber) -> str:
        return str(self.numerator) + '/' + str(self.denominator)