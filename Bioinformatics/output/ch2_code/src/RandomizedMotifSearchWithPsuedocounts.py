from random import randrange
from typing import List, Dict

from FindMostProbableKmerUsingProfileMatrix import find_most_probable_kmer_using_profile_matrix
from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile
from ScoreMotif import score_motif


def increment_counts(count: Dict[str, List[int]]):
    ret = {}
    for elem, counts in count.items():
        ret[elem] = [c + 1 for c in counts]
    return ret


# How to use: Execute this method 1000 or so times and pick the best result out of all the results
def randomized_motif_search_with_psuedocounts(k: int, dnas: List[str]) -> List[str]:
    motifs = []
    for dna in dnas:
        start = randrange(len(dna) - k + 1)
        motif = dna[start:start + k]
        motifs.append(motif)

    best_motifs = motifs

    while True:
        counts_matrix = motif_matrix_count(motifs)
        for elem, counts in counts_matrix.items():  # add in pseudocounts
            counts_matrix[elem] = [c + 1 for c in counts]
        profile_matrix = motif_matrix_profile(counts_matrix)

        motifs = [find_most_probable_kmer_using_profile_matrix(profile_matrix, dna)[0] for dna in dnas]
        if score_motif(motifs) < score_motif(best_motifs):
            best_motifs = motifs
        else:
            return best_motifs


if __name__ == '__main__':
    found_motif_matrix = randomized_motif_search_with_psuedocounts(
        3,
        [
            'GGCGTTCAGGCA',
            'AAGAATCAGTCA',
            'CAAGGAGTTCGC',
            'CACGTCAATCAC',
            'CAATAATATTCG'
        ]
    )

    for motif in found_motif_matrix:
        print(f'{motif}')
