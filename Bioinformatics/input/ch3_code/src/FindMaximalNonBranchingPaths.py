import typing
from collections import Counter
from typing import Dict, TypeVar, List, Optional

from BalanceNearlyBalancedGraph import get_degrees
from Utils import normalize_graph

T = TypeVar('T')


def walk_until_non_1_to_1(graph: Dict[T, typing.Counter[T]], node: T) -> Optional[List[T]]:
    ret = [node]
    while True:
        in_degree, out_degree = get_degrees(graph, node)
        if not(in_degree == 1 and out_degree == 1):
            return ret

        children = graph[node].elements()
        child = next(children)
        if child in ret:
            return None

        node = child
        ret.append(node)


def walk_until_loop(graph: Dict[T, typing.Counter[T]], node: T) -> Optional[List[T]]:
    ret = [node]
    while True:
        children = graph[node].elements()
        child_count = sum(graph[node].values())
        if child_count > 1 or child_count == 0:
            return None

        child = next(children)
        if child in ret:
            return ret

        node = child
        ret.append(node)


def find_maximal_non_branching_paths(graph: Dict[T, typing.Counter[T]]) -> List[List[T]]:
    paths = []

    for node in graph.keys():
        in_degree, out_degree = get_degrees(graph, node)
        if (in_degree == 1 and out_degree == 1) or out_degree == 0:
            continue
        children = graph[node].elements()
        for child in children:
            path_from_child = walk_until_non_1_to_1(graph, child)
            if path_from_child is None:
                continue
            path = [node] + path_from_child
            paths.append(path)

    skip_nodes = set()
    for node in graph.keys():
        if node in skip_nodes:
            continue
        in_degree, out_degree = get_degrees(graph, node)
        if not (in_degree == 1 and out_degree == 1) or out_degree == 0:
            continue
        path = walk_until_loop(graph, node)
        if path is None:
            continue
        path = path + [node]
        paths.append(path)
        skip_nodes |= set(path)

    return paths


if __name__ == '__main__':
    graph = {
        '1': Counter(['2']),
        '2': Counter(['3', '4', '5']),
        '4': Counter(['6', '10']),
        '5': Counter(['7']),
        '6': Counter(['10'])
    }
    graph = normalize_graph(graph)
    for path in find_maximal_non_branching_paths(graph):
        print(f'{"->".join(path)}')
