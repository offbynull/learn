import typing
from collections import Counter
from typing import List, Dict, Set, Tuple, TypeVar

from Utils import find_graph_roots

T = TypeVar('T')


def exhaustively_walk_until_all_nodes_touched_exactly_one(
        graph: Dict[T, typing.Counter[T]],
        from_node: T,
        current_path: List[T]
) -> List[List[T]]:
    current_path.append(from_node)

    if len(current_path) == len(graph):
        found_paths = [current_path.copy()]
    else:
        to_nodes = graph[from_node].keys() - current_path
        found_paths = []
        for to_node in to_nodes:
            found_paths += exhaustively_walk_until_all_nodes_touched_exactly_one(graph, to_node, current_path)

    current_path.pop()
    return found_paths


# walk each node exactly once
def walk_hamiltonian_path(graph: Dict[T, typing.Counter[T]], from_node: T) -> List[List[T]]:
    return exhaustively_walk_until_all_nodes_touched_exactly_one(graph, from_node, [])


# def exhaustively_walk_graph(graph: Dict[T, typing.Counter[T]]) -> List[List[T]]:
#     ret = []
#     root_nodes = find_graph_roots(graph)
#     assert len(root_nodes) > 0  # must have at least 1 root
#     for root_node in root_nodes:
#         paths = walk_hamiltonian_path(graph, root_node)
#         ret += paths
#     return ret
