from typing import List


def bruteforce_probability(searchspace_len: int, searchspace_symbol_count: int, search_for: List[int], min_occurrence: int) -> (int, int):
    found = 0
    found_max = searchspace_symbol_count ** searchspace_len

    str_to_search = [0] * searchspace_len

    def count_instances():
        ret = 0
        for i in range(0, searchspace_len - len(search_for) + 1):
            if str_to_search[i:i + len(search_for)] == search_for:
                ret += 1
        return ret

    def walk(idx: int):
        nonlocal found

        if idx == searchspace_len:
            count = count_instances()
            if count >= min_occurrence:
                found += 1
        else:
            for i in range(0, searchspace_symbol_count):
                walk(idx + 1)
                str_to_search[idx] += 1
            str_to_search[idx] = 0

    walk(0)

    return found, found_max


found, found_max = bruteforce_probability(25, 2, [0, 1], 1)
print(f'{found}/{found_max}')

#  This takes ~7 mins to run, which is not great. There's another solution in the comments that makes use of probability
#  reasoning to come up with a faster computation. I didn't understand how it worked.
