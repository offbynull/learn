import typing
from collections import Counter
from typing import List, Dict

from Utils import normalize_graph, slide_window


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def to_debruijn_graph_from_genome_path(k: int, dna: str) -> Dict[str, typing.Counter[str]]:
    graph = dict()
    for kmer, _ in slide_window(dna, k):
        from_node = prefix(kmer)
        to_node = suffix(kmer)
        graph.setdefault(from_node, Counter())[to_node] += 1
    graph = normalize_graph(graph)
    return graph


# There is no order to the kmers -- this isn't reconstructing from a genome path.
def to_debruijn_graph(kmers: List[str]) -> Dict[str, typing.Counter[str]]:
    graph = dict()
    for kmer in kmers:
        from_node = prefix(kmer)
        to_node = suffix(kmer)
        graph.setdefault(from_node, Counter())[to_node] += 1
    graph = normalize_graph(graph)
    return graph


if __name__ == '__main__':
    dna = 'TAATGCCATGGGATGTT'
    dna_kmers = list([x[0] for x in slide_window(dna, 3)])
    dna_kmers.sort()

    graph1 = to_debruijn_graph_from_genome_path(3, dna)
    for from_node, to_nodes in graph1.items():
        print(f'{from_node} -> {",".join([str(t) for t in dict(to_nodes).items()])}')

    graph2 = to_debruijn_graph(dna_kmers)
    for from_node, to_nodes in graph2.items():
        print(f'{from_node} -> {",".join([str(t) for t in dict(to_nodes).items()])}')

    print(f'{graph1 == graph2}')


# If we gave you the de Bruijn graph DeBruijnk(Text) without giving you Text, could you reconstruct Text?
#   YES. don't walk over same edge more than once

# Construct the de Bruijn graphs DeBruijn2(TAATGCCATGGGATGTT), DeBruijn3(TAATGCCATGGGATGTT), and DeBruijn4(TAATGCCATGGGATGTT). What do you notice?
#   LOWER K: more connections per node, more cycles, less nodes
#   HIGHER K: less connections per node, less cycles, more nodes
# nodes = to_debruijn_graph_from_genome_path(2, 'TAATGCCATGGGATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
# print('---')
# nodes = to_debruijn_graph_from_genome_path(3, 'TAATGCCATGGGATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
# print('---')
# nodes = to_debruijn_graph_from_genome_path(4, 'TAATGCCATGGGATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')

# How does the graph DeBruijn3(TAATGCCATGGGATGTT) compare to DeBruijn3(TAATGGGATGCCATGTT)?
#    SAME GRAPH.
# nodes = to_debruijn_graph_from_genome_path(3, 'TAATGCCATGGGATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
# print('---')
# nodes = to_debruijn_graph_from_genome_path(3, 'TAATGGGATGCCATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
