import typing
from collections import Counter
from typing import List, Dict

from Utils import normalize_graph


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def to_overlap_graph(kmers: List[str]) -> Dict[str, typing.Counter[str]]:
    ret = dict()
    for i, kmer in enumerate(kmers):
        kmer_suffix = suffix(kmer)
        for j, other_kmer in enumerate(kmers):
            if i == j:
                continue
            other_kmer_prefix = prefix(other_kmer)
            if kmer_suffix == other_kmer_prefix:
                ret.setdefault(kmer, Counter())[other_kmer] += 1
    ret = normalize_graph(ret)
    return ret


if __name__ == '__main__':
    out = to_overlap_graph(['ATGCG', 'GCATG', 'CATGC', 'AGGCA', 'GGCAT', 'GGCAC'])
    print(f'{out}')