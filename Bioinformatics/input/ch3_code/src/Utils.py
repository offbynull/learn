from __future__ import annotations

from typing import Tuple

from Kdmer import Kdmer


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
