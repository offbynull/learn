from __future__ import annotations

import typing
from collections import Counter
from typing import Tuple, Dict, TypeVar, Set

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


T = TypeVar('T')


def copy_graph(graph: Dict[T, typing.Counter[T]]) -> Dict[T, typing.Counter[T]]:
    copy = dict()
    for k, v in graph.items():
        copy[k] = v.copy()
    return copy


# make sure every node that appears as a child also appears as a key
def normalize_graph(graph: Dict[T, typing.Counter[T]]) -> Dict[T, typing.Counter[T]]:
    graph = copy_graph(graph)
    all_nodes = graph.keys() | set([node for nodes in graph.values() for node in nodes])
    for n in all_nodes:
        graph.setdefault(n, Counter())
    return graph


def find_graph_roots(graph: Dict[T, typing.Counter[T]]) -> Set[T]:
    nodes_with_incoming_conns = set([n for v in graph.values() for n in v])
    nodes = graph.keys()
    start_nodes = nodes - nodes_with_incoming_conns
    return start_nodes


def count_graph_edges(graph: Dict[T, typing.Counter[T]]) -> int:
    ret = 0
    for from_node in graph.keys():
        ret += len(graph[from_node])
    return ret
