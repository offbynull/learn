from typing import List, Tuple, Dict

from Kdmer import Kdmer


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def bruteforce_overlap_search(kdmers: List[Kdmer]) -> Dict[str, List[str]]:
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
                ret.setdefault(kdmer, []).append(other_kdmer)
    return ret


if __name__ == '__main__':
    # ACTACTGGTACT
    out = bruteforce_overlap_search(
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
