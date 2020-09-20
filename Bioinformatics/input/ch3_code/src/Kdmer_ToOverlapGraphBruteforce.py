import typing
from collections import Counter
from typing import List, Tuple, Dict

from Kdmer import Kdmer
from Utils import normalize_graph


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def to_overlap_graph(kdmers: List[Kdmer]) -> Dict[str, typing.Counter[Kdmer]]:
    ret = dict()
    for i, kdmer in enumerate(kdmers):
        head_suffix = suffix(kdmer.head)
        tail_suffix = suffix(kdmer.tail)
        for j, other_kdmer in enumerate(kdmers):
            if i == j:
                continue
            other_head_prefix = prefix(other_kdmer.head)
            other_tail_prefix = prefix(other_kdmer.tail)
            if head_suffix == other_head_prefix and tail_suffix == other_tail_prefix:
                ret.setdefault(kdmer, Counter())[other_kdmer] += 1
    ret = normalize_graph(ret)
    return ret


if __name__ == '__main__':
    # ACTACTGGTACT
    out = to_overlap_graph(
        [
            Kdmer('ACT', 'CTG', 1),
            Kdmer('CTA', 'TGG', 1),
            Kdmer('TAC', 'GGT', 1),
            Kdmer('ACT', 'GTA', 1),
            Kdmer('CTG', 'TAC', 1),
            Kdmer('TGG', 'ACT', 1)
        ]
    )
    print(f'{out}')
