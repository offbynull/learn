from typing import List

from Utils import normalize_graph


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def debruijn_graph_from_kmers(kmers: List[str]):
    graph = dict()
    for kmer in kmers:
        from_node = prefix(kmer)
        to_node = suffix(kmer)
        graph.setdefault(from_node, []).append(to_node)
    graph = normalize_graph(graph)
    return graph


if __name__ == '__main__':
    graph = debruijn_graph_from_kmers(['GAGG', 'CAGG', 'GGGG', 'GGGA', 'CAGG', 'AGGG', 'GGAG'])
    for kmer, other_kmers in graph.items():
        print(f'{kmer} -> {",".join(other_kmers)}')
