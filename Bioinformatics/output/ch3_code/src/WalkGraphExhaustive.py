import typing
from collections import Counter
from typing import List, Dict, Set, Tuple, TypeVar

from Utils import find_graph_roots

T = TypeVar('T')


def _exhaustively_walk_graph_from_node(
        graph: Dict[T, typing.Counter[T]],
        from_node: T,
        current_path: List[T],
        edges_walked: typing.Counter[Tuple[T, T]]
) -> List[List[T]]:
    current_path = current_path + [from_node]

    to_nodes = graph[from_node]

    found_paths = []
    for to_node, total_conns in to_nodes.items():
        edge = (from_node, to_node)
        edge_walk_count = edges_walked[edge]
        if edge_walk_count < total_conns:
            edges_walked[edge] += 1
            found_paths += _exhaustively_walk_graph_from_node(graph, to_node, current_path[:], edges_walked.copy())

    if len(found_paths) == 0:
        found_paths = [current_path]

    return found_paths


def exhaustively_walk_graph_from_node(graph: Dict[T, typing.Counter[T]], from_node: T) -> List[List[T]]:
    return _exhaustively_walk_graph_from_node(graph, from_node, [], Counter())


def exhaustively_walk_graph(graph: Dict[T, typing.Counter[T]]) -> List[List[T]]:
    ret = []
    root_nodes = find_graph_roots(graph)
    assert len(root_nodes) > 0  # must have at least 
    for root_node in root_nodes:
        paths = exhaustively_walk_graph_from_node(graph, root_node)
        ret += paths
    return ret
