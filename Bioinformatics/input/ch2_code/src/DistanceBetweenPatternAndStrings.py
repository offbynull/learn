from typing import List

from HammingDistanceBetweenKmers import hamming_distance
from Utils import slide_window


# The name is slightly confusing. What this actually does...
#   For each dna string:
#     Get minimum hamming distance between the k-mers that make up the DNA string and pattern
#   Sum up the minimum hamming_dists
def distance_between_pattern_and_strings(pattern: str, dnas: List[str]) -> int:
    min_hds = []

    k = len(pattern)
    for dna in dnas:
        min_hd = None
        for dna_kmer, _ in slide_window(dna, k):
            hd = hamming_distance(pattern, dna_kmer)
            if min_hd is None or hd < min_hd:
                min_hd = hd
        min_hds.append(min_hd)
    return sum(min_hds)


if __name__ == '__main__':
    min_dist = distance_between_pattern_and_strings(
        'aaa',
        [
            'ttaccttAAC'.lower(),
            'gATAtctgtc'.lower(),
            'ACGgcgttcg'.lower(),
            'ccctAAAgag'.lower(),
            'cgtcAGAggt'.lower()
        ]
    )

    print(f'{min_dist}')
