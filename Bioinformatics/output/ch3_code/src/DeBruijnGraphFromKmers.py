from typing import List


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def debruijn_graph_from_kmers(kmers: List[str]):
    nodes = dict()
    for kmer in kmers:
        from_node = prefix(kmer)
        to_node = suffix(kmer)
        nodes.setdefault(from_node, []).append(to_node)
    return nodes


if __name__ == '__main__':
    nodes = debruijn_graph_from_kmers(['GAGG', 'CAGG', 'GGGG', 'GGGA', 'CAGG', 'AGGG', 'GGAG'])
    for kmer, other_kmers in nodes.items():
        print(f'{kmer} -> {",".join(other_kmers)}')
