from __future__ import annotations

from Factor import factor_fastest
from Output import log_decorator, log, log_indent, log_unindent
from WholeNumber import WholeNumber


#MARKDOWN_NAIVE
@log_decorator
def gcd_naive(num1: WholeNumber, num2: WholeNumber) -> WholeNumber:
    log(f'Calculating gcd for {num1} and {num2}...')
    log_indent()

    log(f'Sorting to determine smaller input...')
    min_num = min(num1, num2)

    log(f'Testing up to smaller input ({min_num})...')
    log_indent()
    for i in WholeNumber.range(WholeNumber('1'), min_num, True):
        log(f'Testing {i}...')
        quotient1, remainder1 = num1 / i
        quotient2, remainder2 = num2 / i
        if remainder1 == 0 and remainder2 == 0:
            log(f'{num1} and {num2} are both divisible by {i}...')
            found = i
        else:
            log(f'{num1} and {num2} are NOT both divisible by {i}...')
    log_unindent()

    log_unindent()
    log(f'GCD is {found}')
    return found
#MARKDOWN_NAIVE


#MARKDOWN_FACTOR
@log_decorator
def gcd_factor(num1: WholeNumber, num2: WholeNumber) -> WholeNumber:
    log(f'Calculating gcd for {num1} and {num2}...')
    log_indent()

    log(f'Calculating factors for {num1}...')
    factors1 = factor_fastest(num1)
    log(f'Factors for {num1}: {factors1}')

    log(f'Calculating factors for {num2}...')
    factors2 = factor_fastest(num2)
    log(f'Factors for {num2}: {factors2}')

    log(f'Finding common factors...')
    common_factors = factors1 & factors2  # set intersection
    log(f'Common factors for {num1} and {num2}: {common_factors}')

    found = max(common_factors)

    log_unindent()
    log(f'GCD is {found}')
    return found
#MARKDOWN_FACTOR


if __name__ == '__main__':
    print(f'{gcd_factor(WholeNumber("22"), WholeNumber("8"))}')
