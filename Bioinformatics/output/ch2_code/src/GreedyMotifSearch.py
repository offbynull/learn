from typing import List

from FindMostProbableKmerUsingProfileMatrix import find_most_probable_kmer_using_profile_matrix
from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile
from ScoreMotif import score_motif
from Utils import slide_window


def greedy_motif_search(k: int, dnas: List[str]):
    best_motif_matrix = [dna[0:k] for dna in dnas]

    for motif, _ in slide_window(dnas[0], k):
        motif_matrix = [motif]
        counts = motif_matrix_count(motif_matrix)
        profile = motif_matrix_profile(counts)

        for dna in dnas[1:]:
            next_motif, _ = find_most_probable_kmer_using_profile_matrix(profile, dna)
            # pop in closest kmer as a motif and recompute profile for the next iteration
            motif_matrix.append(next_motif)
            counts = motif_matrix_count(motif_matrix)
            profile = motif_matrix_profile(counts)

        if score_motif(motif_matrix) < score_motif(best_motif_matrix):
            best_motif_matrix = motif_matrix

    return best_motif_matrix


if __name__ == '__main__':
    found_motif_matrix = greedy_motif_search(
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
