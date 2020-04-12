from __future__ import annotations

from typing import Dict, List

from FindClumpsOfAKnownKmer import find_kmer_clusters
from CountASequencesKmers import kmer_frequency


# MARKDOWN
def find_clustered_kmers(sequence: str, k: int, min_occurrence_in_cluster: int, cluster_window_size: int) -> Dict[str, List[int]]:
    ret = {}

    unique_kmers = kmer_frequency(sequence, k)
    for kmer in unique_kmers:
        idxes = find_kmer_clusters(sequence, kmer, min_occurrence_in_cluster, cluster_window_size)
        if len(idxes) > 0:
            ret[kmer] = idxes

    return ret
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        k = int(input())
        min_occurrence_in_cluster = int(input())
        cluster_window_size = int(input())
        print(f'Searching {seq} for clusters of {k}-mer where at least {min_occurrence_in_cluster} occurrences exist in window of {cluster_window_size}\n')
        clusters = find_clustered_kmers(seq, k, min_occurrence_in_cluster, cluster_window_size)
        print(f'Found the following clusters:')
        [print(f' * {kmer}: {idxes}') for kmer, idxes in clusters.items()]
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()