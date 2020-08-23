from random import randrange
from typing import List, Dict

from FindMostProbableKmerUsingProfileMatrix import find_most_probable_kmer_using_profile_matrix, \
    apply_psuedocounts_to_count_matrix
from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile
from ScoreMotif import score_motif


# How to use: Execute this method 1000 or so times and pick the best result out of all the results
# MARKDOWN
def randomized_motif_search_with_psuedocounts(k: int, dnas: List[str]) -> List[str]:
    motifs = []
    for dna in dnas:
        start = randrange(len(dna) - k + 1)
        motif = dna[start:start + k]
        motifs.append(motif)

    best_motifs = motifs

    while True:
        counts_matrix = motif_matrix_count(motifs)
        apply_psuedocounts_to_count_matrix(counts_matrix)
        profile_matrix = motif_matrix_profile(counts_matrix)

        motifs = [find_most_probable_kmer_using_profile_matrix(profile_matrix, dna)[0] for dna in dnas]
        if score_motif(motifs) < score_motif(best_motifs):
            best_motifs = motifs
        else:
            return best_motifs
# MARKDOWN


# EXAMPLE INPUT: (make sure to send EOF signal to begin processing, it may take forever to finish)
#
# 1000
# 3
# AAATTGACGCAT
# GACGACCACGTT
# CGTCAGCGCCTG
# GCTGAGCACCGG
# AGTTCGGGACAG

def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        iterations = int(input())
        k = int(input())
        dnas = []
        while True:
            try:
                dna = input().strip().upper()
                if len(dna) > 0:
                    dnas.append(dna)
            except EOFError:
                break

        print(f'Searching for motif of k={k} in the following...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        print(f'Running {iterations} iterations...\n\n')

        best_motif_matrix = None
        for iteration in range(iterations):
            found_motif_matrix = randomized_motif_search_with_psuedocounts(k, dnas)
            if best_motif_matrix is None or score_motif(found_motif_matrix) < score_motif(best_motif_matrix):
                best_motif_matrix = found_motif_matrix

        print(f'Best found the motif matrix...\n\n')
        print(f'{"<br>".join(best_motif_matrix)}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()