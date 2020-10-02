from typing import List, TypeVar

from Graph import Graph
from Read import Read
from Utils import slide_window

T = TypeVar('T')


def to_debruijn_graph(reads: List[T], skip: int = 1) -> Graph[T]:
    graph = Graph()
    for read in reads:
        from_node = read.prefix(skip)
        to_node = read.suffix(skip)
        graph.insert_edge(from_node, to_node)
    return graph


if __name__ == '__main__':
    dna = 'TAATGCCATGGGATGTT'
    reads = list([Read(x) for x, _ in slide_window(dna, 3)])
    reads.sort(key=lambda x: str(x))

    graph = to_debruijn_graph(reads)
    for from_node, to_nodes in graph.get_all_outputs():
        print(f'{from_node} -> {",".join([str(t) for t in to_nodes])}')


# If we gave you the de Bruijn graph DeBruijn_k(Text) without giving you Text, could you reconstruct Text?
#   YES. don't walk over same edge more than once

# Construct the de Bruijn graphs DeBruijn_2(TAATGCCATGGGATGTT), DeBruijn_3(TAATGCCATGGGATGTT), and DeBruijn_4(TAATGCCATGGGATGTT). What do you notice?
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

# How does the graph DeBruijn_3(TAATGCCATGGGATGTT) compare to DeBruijn_3(TAATGGGATGCCATGTT)?
#    SAME GRAPH.
# nodes = to_debruijn_graph_from_genome_path(3, 'TAATGCCATGGGATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
# print('---')
# nodes = to_debruijn_graph_from_genome_path(3, 'TAATGGGATGCCATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
