from typing import List, TypeVar

from Graph import Graph
from ReadPair import ReadPair
from ToOverlapGraphHash import to_overlap_graph
from Utils import slide_window_kd

T = TypeVar('T')


# MARKDOWN
def exhaustively_walk_until_all_nodes_touched_exactly_one(
        graph: Graph[T],
        from_node: T,
        current_path: List[T]
) -> List[List[T]]:
    current_path.append(from_node)

    if len(current_path) == len(graph):
        found_paths = [current_path.copy()]
    else:
        found_paths = []
        for to_node in graph.get_outputs(from_node):
            if to_node in set(current_path):
                continue
            found_paths += exhaustively_walk_until_all_nodes_touched_exactly_one(graph, to_node, current_path)

    current_path.pop()
    return found_paths


# walk each node exactly once
def walk_hamiltonian_path(graph: Graph[T], from_node: T) -> List[List[T]]:
    return exhaustively_walk_until_all_nodes_touched_exactly_one(graph, from_node, [])
# MARKDOWN


if __name__ == '__main__':
    readpairs = [ReadPair(kdmer) for kdmer, _ in slide_window_kd('TAATGCCATGGGATGTT', 3, 1)]
    graph = to_overlap_graph(readpairs)

    dnas = set()
    for node in graph.get_nodes():
        paths = walk_hamiltonian_path(graph, node)
        for path in paths:
            dna = path[0].stitch(path)
            dnas.add(dna)

    for dna in dnas:
        print(f'{dna}')
