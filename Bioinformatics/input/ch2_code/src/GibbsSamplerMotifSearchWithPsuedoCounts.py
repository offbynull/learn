from collections import Counter
from random import randrange, random, uniform
from typing import List, Dict

from FindMostProbableKmerUsingProfileMatrix import determine_probability_of_match_using_profile_matrix
from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile
from ScoreMotif import score_motif
from Utils import slide_window


def gibbs_rand(prob_dist: List[float]) -> int:
    # normalize prob_dist -- just incase sum(prob_dist) != 1.0
    prob_dist_sum = sum(prob_dist)
    prob_dist = [p / prob_dist_sum for p in prob_dist]

    while True:
        selection = randrange(0, len(prob_dist))
        if random() < prob_dist[selection]:
            return selection


def determine_probabilities_of_all_kmers_in_dna(profile_matrix: Dict[str, List[float]], dna: str, k: int) -> List[int]:
    ret = []
    for kmer, _ in slide_window(dna, k):
        prob = determine_probability_of_match_using_profile_matrix(profile_matrix, kmer)
        ret.append(prob)
    return ret


def gibbs_sampler_motif_search_with_psuedocounts(k: int, dnas: List[str], cycles: int) -> List[str]:
    motifs = []
    for dna in dnas:
        start = randrange(len(dna) - k + 1)
        motif = dna[start:start + k]
        motifs.append(motif)

    best_motifs = motifs[:]  # create a copy, otherwise you'll be modifying both motif and best_motif

    for j in range(0, cycles):
        i = randrange(len(dnas))  # pick a dna
        del motifs[i]  # remove the kmer for that dna from the motif str

        counts_matrix = motif_matrix_count(motifs)
        for elem, counts in counts_matrix.items():  # add in pseudocounts
            counts_matrix[elem] = [c + 1 for c in counts]
        profile_matrix = motif_matrix_profile(counts_matrix)

        new_motif_kmer_probs = determine_probabilities_of_all_kmers_in_dna(profile_matrix, dnas[i], k)
        new_motif_kmer_idx = gibbs_rand(new_motif_kmer_probs)
        new_motif_kmer = dnas[i][new_motif_kmer_idx:new_motif_kmer_idx+k]
        motifs.insert(i, new_motif_kmer)

        if score_motif(motifs) < score_motif(best_motifs):
            best_motifs = motifs[:]  # create a copy, otherwise you'll be modifying both motif and best_motif

    return best_motifs


if __name__ == '__main__':
    found_motif_matrix = gibbs_sampler_motif_search_with_psuedocounts(
        8,
        [
            'CGCCCCTCTCGGGGGTGTTCAGTAACCGGCCA',
            'GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG',
            'TAGTACCGAGACCGAAAGAAGTATACAGGCGT',
            'TAGATCAAGTTTCAGGTGCACGTCGGTGAACC',
            'AATCCACCAGCTCCACGTGCAATGTTGGCCTA'
        ],
        1000
    )

    for motif in found_motif_matrix:
        print(f'{motif}')

    # Test rng to make sure its returning proper distributions
    # c = Counter()
    # for i in range(100000):
    #     c[gibbs_rand([0.1, 0.2, 0.3])] += 1
    # print(f'{c}')