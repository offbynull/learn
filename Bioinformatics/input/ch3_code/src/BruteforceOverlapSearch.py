from typing import List, Tuple, Dict


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def bruteforce_find_overlaps(kmers: List[str]) -> Dict[str, List[str]]:
    ret = dict()
    for i, kmer in enumerate(kmers):
        kmer_suffix = suffix(kmer)
        for j, other_kmer in enumerate(kmers):
            if i == j:
                continue
            other_kmer_prefix = prefix(other_kmer)
            if kmer_suffix == other_kmer_prefix:
                ret.setdefault(kmer, []).append(other_kmer)
    return ret


if __name__ == '__main__':
    out = bruteforce_find_overlaps(['ATGCG', 'GCATG', 'CATGC', 'AGGCA', 'GGCAT', 'GGCAC'])
    print(f'{out}')