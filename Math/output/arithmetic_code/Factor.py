from __future__ import annotations
from typing import Set, Tuple, List, Optional

from WholeNumber import WholeNumber


def factor_naive(num: WholeNumber) -> Set[WholeNumber]:
    ret: Set[WholeNumber] = set()
    for factor1 in WholeNumber.range(WholeNumber(1), num, end_inclusive=True):
        for factor2 in WholeNumber.range(WholeNumber(1), num, end_inclusive=True):
            if factor1 * factor2 == num:
                ret.add(factor1)
                ret.add(factor2)
                print(f'{factor1} {factor2}')
    return ret


def factor_fast(num: WholeNumber) -> Set[WholeNumber]:
    ret: Set[WholeNumber] = set()
    for factor1 in WholeNumber.range(WholeNumber(1), num, end_inclusive=True):
        factor2, remainder = num / factor1
        if remainder == WholeNumber(0):
            ret.add(factor1)
            ret.add(factor2)
            print(f'{factor1} {factor2}')
    return ret


def factor_fastest(num: WholeNumber) -> Set[WholeNumber]:
    ret: Set[WholeNumber] = set()
    for factor1 in WholeNumber.range(WholeNumber(1), num, end_inclusive=True):
        factor2, remainder = num / factor1
        if remainder == WholeNumber(0):
            ret.add(factor1)
            ret.add(factor2)
            print(f'{factor1} {factor2}')
        if factor2 <= factor1:
            break
    return ret


def is_prime(num: WholeNumber) -> bool:
    num_factors = factor_fastest(num)
    print(f'{num}\'s factors are {num_factors}')

    # At a minimum, all counting numbers have the factors 1 and the number itself (2 factors). If
    # there are more factore than that, it's a composite. Otherwise, it's a primse.

    if len(num_factors) == 2:
        print(f'{num} is a prime');
        return True
    else:
        print(f'{num} is a composite');
        return False


def factor_tree(num: WholeNumber) -> FactorTreeNode:
    factors = factor_fastest(num)

    # remove factor pairs that can't used in factor true: (1, num) or (num, 1)
    factors = set([f for f in factors if f != WholeNumber(1) and f != num])

    ret = FactorTreeNode()
    if len(factors) == 0:
        ret.value = num
    else:
        factor1 = next(iter(factors))
        factor2, _ = num / factor1
        ret.value = num
        ret.left = factor_tree(factor1)
        ret.right = factor_tree(factor2)
    return ret


class FactorTreeNode:
    value: WholeNumber
    left: Optional[FactorTreeNode]
    right: Optional[FactorTreeNode]

    def __init__(self):
        self.left = None
        self.right = None

    def get_prime_factors(self, output_list: List[WholeNumber] = None) -> List[WholeNumber]:
        if output_list is None:
            output_list = []

        if self.left is None and self.right is None:
            output_list.append(self.value)

        if self.left is not None:
            self.left.get_prime_factors(output_list)
        if self.right is not None:
            self.right.get_prime_factors(output_list)

        return output_list


def ladder(num: WholeNumber) -> Set[WholeNumber]:
    prime_factors: List[WholeNumber] = []

    while not is_prime(num):
        prime_to_test = WholeNumber(2)
        while True:
            (new_num, remainder) = num / prime_to_test
            if remainder == WholeNumber(0):
                break
            prime_to_test = calculate_next_prime(prime_to_test)
        prime_factors.append(prime_to_test)
        num = new_num

    prime_factors.append(num)

    return prime_factors


def calculate_next_prime(last_prime: WholeNumber) -> WholeNumber:
    next_possible_prime = last_prime + WholeNumber(1)
    while True:
        if is_prime(next_possible_prime):
            return next_possible_prime
        else:
            next_possible_prime += WholeNumber(1)






if __name__ == '__main__':
    # factors = factor_naive(WholeNumber(24))
    # factors = factor_fast(WholeNumber(24))
    # factors = factor_fastest(WholeNumber(24))
    # print(f'{factors}')
    # print(f'{prime_test(WholeNumber(49))}')
    # tree = factor_tree(WholeNumber(24))
    # print(f'{tree}')
    print(f'{ladder(WholeNumber(24))}')