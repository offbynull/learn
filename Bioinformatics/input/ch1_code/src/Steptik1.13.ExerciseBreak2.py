from typing import List


def factorial(num):
    if num == 1:
        return num
    else:
        return num * factorial(num - 1)


def count(m, k):
    return factorial(m) / (factorial(k) * factorial(m-k))


print(f'{count(5, 2)}')
print(f'{count(476, 3)}')


# approximate probability (slight overestimate) based on the insertion logic discussed in the section just after this
# exercise break -- don't fully follow what's going on in the insertion logic / why it works but whatever
def approximate_probability(searchspace_len: int, searchspace_symbol_count: int, search_for: List[int], min_occurrence: int) -> float:
    k = len(search_for)
    n = (searchspace_len - min_occurrence * k)
    return count(n + min_occurrence, min_occurrence) * (searchspace_symbol_count ** n) / searchspace_symbol_count ** searchspace_len


print(f'{approximate_probability(30, 4, [0,1,3,0,3], 3)}')
