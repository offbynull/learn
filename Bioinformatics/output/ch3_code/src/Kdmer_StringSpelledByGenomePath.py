from typing import List, Tuple

from Kdmer import Kdmer
from Kmer_StringSpelledByGenomePath import string_spelled_by_genome_path as kmer_string_spelled_by_genome_path


def string_spelled_by_genome_path(path: List[Kdmer]) -> str:
    if len(path) == 0:
        return ''

    k = path[0].k
    d = path[0].d
    assert len(path) >= d  # if there aren't at least d elements, it's impossible to reconstruct

    total_prefix = kmer_string_spelled_by_genome_path([kd.head for kd in path])
    total_suffix = kmer_string_spelled_by_genome_path([kd.tail for kd in path])

    non_overlap_count = k+d
    final_prefix = total_prefix[:non_overlap_count]
    final_overlap1 = total_prefix[non_overlap_count:]
    final_overlap2 = total_suffix[:-non_overlap_count]
    final_suffix = total_suffix[-non_overlap_count:]

    ret = final_prefix
    for ch1, ch2 in zip(final_overlap1, final_overlap2):
        ret += ch1 if ch1 == ch2 else '?'  # for failure, use IUPAC nucleotide codes instead of question mark?
    ret += final_suffix

    return ret


if __name__ == '__main__':
    out = string_spelled_by_genome_path(
        [
            Kdmer('AG', 'AG', 1),
            Kdmer('GC', 'GC', 1),
            Kdmer('CA', 'CT', 1),
            Kdmer('AG', 'TG', 1),
            Kdmer('GC', 'GC', 1),
            Kdmer('CT', 'CT', 1),
            Kdmer('TG', 'TG', 1),
            Kdmer('GC', 'GC', 1),
            Kdmer('CT', 'CA', 1)
        ]
    )
    print(f'{out}')
