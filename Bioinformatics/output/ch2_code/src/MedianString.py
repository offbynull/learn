from typing import List, Tuple

from DistanceBetweenPatternAndStrings import distance_between_pattern_and_strings
from Utils import enumerate_patterns


def median_string(k: int, dnas: List[str]):
    last_found: Tuple[str, int] = None  # last found patter and its distance,
    for kmer in enumerate_patterns(k):
        dist = distance_between_pattern_and_strings(kmer, dnas)
        if last_found is None or dist < last_found[1]:
            last_found = kmer, dist
    return last_found


if __name__ == '__main__':
    ret = median_string(
        3,
        [
            'AAATTGACGCAT',
            'GACGACCACGTT',
            'CGTCAGCGCCTG',
            'GCTGAGCACCGG',
            'AGTTCGGGACAG'
        ]
    )
    print(f'{ret}')