from __future__ import annotations

from random import Random
from typing import Tuple, Optional

from Kdmer import Kdmer


def count_kmers(data_len: int, k: int) -> int:
    return data_len - k + 1


def slide_window(data: str, k: int) -> Tuple[str, int]:
    for i in range(0, len(data) - k + 1):
        yield data[i:i+k], i


def slide_window_kd(data: str, k: int, d: int) -> Tuple[Kdmer, int]:
    for a, b in zip(slide_window(data, k), slide_window(data[k+d:], k)):
        yield Kdmer(a[0], b[0], d), a[1]


def enumerate_patterns(k: int, elements='ACGT') -> str:
    def inner(current: str, k: int, elements: str):
        if k == 0:
            yield current
        else:
            for element in elements:
                yield from inner(current + element, k - 1, elements)

    yield from inner('', k, elements)


def generate_random_genome(size: int, r: Optional[Random] = None) -> str:
    if r is None:
        r = Random()
    return ''.join([r.choice(['A', 'C', 'T', 'G']) for i in range(size)])


def complement_genome(data: str) -> str:
    new_data = ''
    for ch in reversed(data):
        if ch == 'A':
            ch = 'T'
        elif ch == 'T':
            ch = 'A'
        elif ch == 'C':
            ch = 'G'
        elif ch == 'G':
            ch = 'C'
        new_data += ch
    return new_data
