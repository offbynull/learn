from typing import List

from Utils import slide_window


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def string_to_debruijn_graph(kmers: List[str]):
    nodes = dict()
    for kmer, _ in slide_window(dna, k):
        from_node = prefix(kmer)
        to_node = suffix(kmer)
        nodes.setdefault(from_node, []).append(to_node)
    return nodes


if __name__ == '__main__':
    nodes = string_to_debruijn_graph(3, 'TAATGCCATGGGATGTT')
    for kmer, other_kmers in nodes.items():
        print(f'{kmer} -> {",".join(other_kmers)}')

    # If we gave you the de Bruijn graph DeBruijnk(Text) without giving you Text, could you reconstruct Text?
    #   YES. don't walk over same edge more than once

    # Construct the de Bruijn graphs DeBruijn2(TAATGCCATGGGATGTT), DeBruijn3(TAATGCCATGGGATGTT), and DeBruijn4(TAATGCCATGGGATGTT). What do you notice?
    #   LOWER K: more connections per node, more cycles, less nodes
    #   HIGHER K: less connections per node, less cycles, more nodes
    # nodes = string_to_debruijn_graph(2, 'TAATGCCATGGGATGTT')
    # for kmer, other_kmers in nodes.items():
    #     print(f'{kmer} -> {",".join(other_kmers)}')
    # print('---')
    # nodes = string_to_debruijn_graph(3, 'TAATGCCATGGGATGTT')
    # for kmer, other_kmers in nodes.items():
    #     print(f'{kmer} -> {",".join(other_kmers)}')
    # print('---')
    # nodes = string_to_debruijn_graph(4, 'TAATGCCATGGGATGTT')
    # for kmer, other_kmers in nodes.items():
    #     print(f'{kmer} -> {",".join(other_kmers)}')

    # How does the graph DeBruijn3(TAATGCCATGGGATGTT) compare to DeBruijn3(TAATGGGATGCCATGTT)?
    #    SAME GRAPH.
    # nodes = string_to_debruijn_graph(3, 'TAATGCCATGGGATGTT')
    # for kmer, other_kmers in nodes.items():
    #     print(f'{kmer} -> {",".join(other_kmers)}')
    # print('---')
    # nodes = string_to_debruijn_graph(3, 'TAATGGGATGCCATGTT')
    # for kmer, other_kmers in nodes.items():
    #     print(f'{kmer} -> {",".join(other_kmers)}')