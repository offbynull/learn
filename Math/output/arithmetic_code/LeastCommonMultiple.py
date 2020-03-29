from __future__ import annotations

from collections import Counter
from typing import List, Tuple, Set

from Factor import factor_tree
from WholeNumber import WholeNumber


def lcm_walk(num1: WholeNumber, num2: WholeNumber) -> Tuple[List[WholeNumber], List[WholeNumber]]:
    num1_multiples: List[WholeNumber] = []
    num2_multiples: List[WholeNumber] = []

    num1_counter = WholeNumber(1)
    num2_counter = WholeNumber(1)

    num1_multiple = num1 * num1_counter
    num1_multiples.append(num1_multiple)

    num2_multiple = num2 * num2_counter
    num2_multiples.append(num2_multiple)

    while True:
        if num1_multiple < num2_multiple:
            # num1Multiple is less than num2Multiple, increase it
            num1_counter += WholeNumber(1)
            num1_multiple = num1 * num1_counter
            num1_multiples.append(num1_multiple)
        elif num1_multiple > num2_multiple:
            # num2Multiple is less than num1Multiple, increase it
            num2_counter += WholeNumber(1)
            num2_multiple = num2 * num2_counter
            num2_multiples.append(num2_multiple)
        else:
            # multiples match -- we're done.
            break

    return num1_multiples, num2_multiples


def lcm_prime_factorize(num1: WholeNumber, num2: WholeNumber) -> WholeNumber:
    num1_primes = sorted(factor_tree(num1).get_prime_factors())
    num2_primes = sorted(factor_tree(num2).get_prime_factors())

    distinct_primes: Set[WholeNumber] = set()
    [distinct_primes.add(p) for p in num1_primes]
    [distinct_primes.add(p) for p in num2_primes]

    least_common_multiple = WholeNumber(1)
    least_common_multiple_primes = Counter()
    for prime in sorted(list(distinct_primes)):
        num1_count = num1_primes.count(prime)
        num2_count = num2_primes.count(prime)
        if num1_count >= num2_count:
            for i in WholeNumber.range(WholeNumber(0), WholeNumber(num1_count)):
                least_common_multiple = least_common_multiple * prime
            least_common_multiple_primes[prime] += num1_count
        else:
            for i in WholeNumber.range(WholeNumber(0), WholeNumber(num2_count)):
                least_common_multiple = least_common_multiple * prime
            least_common_multiple_primes[prime] += num2_count

    return least_common_multiple, least_common_multiple_primes


if __name__ == '__main__':
    print(f'{lcm_walk(WholeNumber(6), WholeNumber(7))}')
    print(f'{lcm_prime_factorize(WholeNumber(6), WholeNumber(7))}')