from typing import List, Dict

from Kdmer import Kdmer


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def hash_overlap_search(kdmers: List[Kdmer]) -> Dict[str, List[Kdmer]]:
    ret = dict()

    prefixes = dict()
    suffixes = dict()
    for i, kdmer in enumerate(kdmers):
        head_prefix = prefix(kdmer.head)
        head_suffix = suffix(kdmer.head)
        tail_prefix = prefix(kdmer.tail)
        tail_suffix = suffix(kdmer.tail)
        prefixes.setdefault((head_prefix, tail_prefix), set()).add(i)
        suffixes.setdefault((head_suffix, tail_suffix), set()).add(i)

    for key, indexes in suffixes.items():
        other_indexes = prefixes.get(key)
        if other_indexes is None:
            continue
        for i in indexes:
            kdmer = kdmers[i]
            for j in other_indexes:
                if i == j:
                    continue
                other_kdmer = kdmers[j]
                ret.setdefault(kdmer, []).append(other_kdmer)

    return ret


if __name__ == '__main__':
    # ACTACTGGTACT
    out = hash_overlap_search(
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
