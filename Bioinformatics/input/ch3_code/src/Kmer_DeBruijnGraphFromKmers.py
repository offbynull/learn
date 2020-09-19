import typing
from collections import Counter
from typing import List, Dict

from Utils import normalize_de_bruijn_graph


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


# There is no order to the kmers -- this isn't reconstructing from a genome path.
def debruijn_graph_from_kmers(kmers: List[str]) -> Dict[str, typing.Counter[str]]:
    graph = dict()
    for kmer in kmers:
        from_node = prefix(kmer)
        to_node = suffix(kmer)
        graph.setdefault(from_node, Counter())[to_node] += 1
    graph = normalize_de_bruijn_graph(graph)
    return graph


if __name__ == '__main__':
    graph = debruijn_graph_from_kmers(['GAGG', 'CAGG', 'GGGG', 'GGGA', 'CAGG', 'AGGG', 'GGAG'])
    for from_node, to_nodes in graph.items():
        print(f'{from_node} -> {",".join([str(t) for t in dict(to_nodes).items()])}')
