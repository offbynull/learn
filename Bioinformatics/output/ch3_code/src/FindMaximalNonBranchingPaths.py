import typing
from typing import Dict, TypeVar, List

from BalanceNearlyBalancedGraph import get_degrees

T = TypeVar('T')


def walk_until_branch_or_loop(graph: Dict[T, typing.Counter[T]], node: T) -> List[T]:
    ret = [node]
    while True:
        children = graph[node].elements()
        child_count = sum(children)
        if child_count > 1 or child_count == 0:
            return ret

        child = next(children)
        if child in ret:
            return ret

        node = child


def find_maximal_non_branching_paths(graph: Dict[T, typing.Counter[T]]) -> List[List[T]]:
    remaining_nodes = set(graph.keys())
    while remaining_nodes:
        node = remaining_nodes.pop()
        in_degree, out_degree = get_degrees(graph, node)
        if in_degree != out_degree:

    pass