from __future__ import annotations
from typing import Set, Tuple

from WholeNumber import WholeNumber


def factor_naive(num: WholeNumber) -> Set[Tuple[WholeNumber, WholeNumber]]:
    ret: Set[Tuple[WholeNumber, WholeNumber]] = set()
    for factor1 in WholeNumber.range(WholeNumber(1), num, end_inclusive=True):
        for factor2 in WholeNumber.range(WholeNumber(1), num, end_inclusive=True):
            if factor1 * factor2 == num:
                ret.add((factor1, factor2))
                print(f'{factor1} {factor2}')
    return ret


def factor_fast(num: WholeNumber) -> Set[Tuple[WholeNumber, WholeNumber]]:
    ret: Set[Tuple[WholeNumber, WholeNumber]] = set()
    for factor1 in WholeNumber.range(WholeNumber(1), num, end_inclusive=True):
        factor2, remainder = num / factor1
        if remainder == WholeNumber(0):
            ret.add((factor1, factor2))
            print(f'{factor1} {factor2}')
    return ret


def factor_fastest(num: WholeNumber) -> Set[Tuple[WholeNumber, WholeNumber]]:
    ret: Set[Tuple[WholeNumber, WholeNumber]] = set()
    for factor1 in WholeNumber.range(WholeNumber(1), num, end_inclusive=True):
        factor2, remainder = num / factor1
        if remainder == WholeNumber(0):
            ret.add((factor1, factor2))
            print(f'{factor1} {factor2}')
        if factor2 <= factor1:
            break
    return ret


def prime_test(num: WholeNumber) -> WholeNumber:
    num_factors = factor_fastest(num)
    print(f'{num}\'s factors are {num_factors}')

    # At a minimum, all counting numbers have the factors 1 and the number itself (2 factors). If
    # there are more factore than that, it's a composite. Otherwise, it's a primse.

    if len(num_factors) == 2:
        print(f'{num} is a prime');
    else:
        print(f'{num} is a composite');

def factor_tree(num: WholeNumber) -> FactorTreeNode:
    factor_pairs = factor_fastest(num)

    # remove factor pairs that can't used in factor true: (1, num) or (num, 1)
    factor_pairs = set([fp for fp in factor_pairs if fp[0] != WholeNumber(1) and fp[1] != WholeNumber(1)])

    ret = FactorTreeNode()
    if len(factor_pairs) == 0:
        ret.value = num
    else:
        factor_pair = next(iter(factor_pairs))
        ret.value = num
        ret.left = factor_tree(factor_pair[0])
        ret.right = factor_tree(factor_pair[1])
    return ret


class FactorTreeNode:
    value: WholeNumber
    left: FactorTreeNode
    right: FactorTreeNode

LADDER?
LIST LEAST COMMON MULTIPLE
PRIME FACTORIZE LIST COMMON MULTIPLES






if __name__ == '__main__':
    # factors = factor_naive(WholeNumber(24))
    # factors = factor_fast(WholeNumber(24))
    # factors = factor_fastest(WholeNumber(24))
    # print(f'{factors}')
    # print(f'{prime_test(WholeNumber(49))}')
    tree = factor_tree(WholeNumber(24))