import typing
from collections import Counter
from typing import List, Dict, Set, Tuple

from Kmer_HashOverlapSearch import hash_overlap_search
from Kmer_StringComposition import string_composition
from Kmer_StringSpelledByGenomePath import string_spelled_by_genome_path
from Utils import normalize_graph


def find_graph_roots(graph: Dict[str, List[str]]) -> Set[str]:
    nodes_with_incoming_conns = set([n for v in graph.values() for n in v])
    nodes = graph.keys()
    start_nodes = nodes - nodes_with_incoming_conns
    return start_nodes


def get_edge_count(graph: Dict[str, List[str]]) -> int:
    ret = 0
    for from_node in graph.keys():
        ret += len(graph[from_node])
    return ret


def walk_overlap_graph_from_node(graph: Dict[str, List[str]], from_node: str, current_path: List[str], edges_walked: typing.Counter[Tuple[str, str]]) -> List[List[str]]:
    current_path = current_path + [from_node]

    to_nodes = graph[from_node]
    if len(to_nodes) == 0:
        return [current_path]

    found_paths = []
    for to_node in to_nodes:
        max_walks = to_nodes.count(to_node)
        edge = (from_node, to_node)
        edge_walk_count = edges_walked[edge]
        if edge_walk_count < max_walks:
            edges_walked[edge] += 1
            found_paths += walk_overlap_graph_from_node(graph, to_node, current_path[:], edges_walked.copy())

    return found_paths


def walk_overlap_graph(graph: Dict[str, List[str]]) -> List[List[str]]:
    ret = []
    root_nodes = find_graph_roots(graph)
    for root_node in root_nodes:
        paths = walk_overlap_graph_from_node(graph, root_node, [], Counter())
        ret += paths
    return ret


if __name__ == '__main__':
    kmers = string_composition(3, 'TAATGCCATGGGATGTT')
    graph = hash_overlap_search(kmers)
    graph = normalize_graph(graph)
    total_edges_count = get_edge_count(graph)
    paths = walk_overlap_graph(graph)
    paths_set = set([tuple(p) for p in paths])
    for path in paths_set:
        dna = string_spelled_by_genome_path(path)
        print(f'{dna} -- {len(set(path))} of {len(graph.keys())} nodes walked')