from time import time
from collections import Counter
from math import factorial
from typing import Dict, Set

with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

start_time = time()

expected_mass = int(data.strip())
weights_table = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]


class HashableCounter(Counter):
    def __init__(self, v=None):
        super().__init__(v)
        self._cached_hash = None

    def __hash__(self):
        if self._cached_hash is None:
            self._cached_hash = hash(tuple(sorted(self.items())))
        return self._cached_hash

    def __str__(self):
        return '+'.join([str(k) + '*' + str(v) for k, v in sorted(self.items())])

    def __repr__(self):
        return str(self)


cache = {0: {HashableCounter()}}
all_cache = cache.copy()

found = set()
while len(cache) > 0:
    new_cache = dict()
    for mass, possibilities in cache.items():
        for w in weights_table:
            new_mass = mass + w
            if new_mass > expected_mass:
                continue

            distance_to_expected_mass = expected_mass - new_mass
            if distance_to_expected_mass in all_cache:
                remainders = all_cache[distance_to_expected_mass]
                for r in remainders:
                    for p in possibilities:
                        p = HashableCounter(p + r)
                        p[w] += 1
                        found.add(p)
            else:
                new_possibilities = set()
                for p in possibilities:
                    p = HashableCounter(p)
                    p[w] += 1
                    new_possibilities.add(p)
                if new_mass < expected_mass:
                    new_cache.setdefault(new_mass, set()).update(new_possibilities)
                    all_cache.setdefault(new_mass, set()).update(new_possibilities)
                elif new_mass == expected_mass:
                    found |= new_possibilities
    cache = new_cache


perms = []
for f in found:
    # https://math.stackexchange.com/a/1356034
    numer = factorial(len(list(f.elements())))
    denom = 1
    for weight, count in f.items():
        denom *= factorial(count)
    permutations_without_dupes = numer // denom
    print(f'{f} = {permutations_without_dupes}')
    perms.append(permutations_without_dupes)
print(f'{sum(perms)}')


print(f'{time() - start_time}')
