from typing import List, Dict


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def hash_overlap_search(kmers: List[str]) -> Dict[str, List[str]]:
    ret = dict()

    prefixes = dict()
    suffixes = dict()
    for i, kmer in enumerate(kmers):
        kmer_prefix = prefix(kmer)
        prefixes.setdefault(kmer_prefix, set()).add(i)
        kmer_suffix = suffix(kmer)
        suffixes.setdefault(kmer_suffix, set()).add(i)

    for key, indexes in suffixes.items():
        other_indexes = prefixes.get(key)
        if other_indexes is None:
            continue
        for i in indexes:
            kmer = kmers[i]
            for j in other_indexes:
                if i == j:
                    continue
                other_kmer = kmers[j]
                ret.setdefault(kmer, []).append(other_kmer)

    return ret


if __name__ == '__main__':
    out = hash_overlap_search(['ATGCG', 'GCATG', 'CATGC', 'AGGCA', 'GGCAT', 'GGCAC'])
    print(f'{out}')