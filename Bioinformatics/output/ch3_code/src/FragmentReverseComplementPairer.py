from collections import Counter
from random import Random
from typing import Dict, List, TypeVar, Optional, Tuple

from FragmentOccurrenceProbabilityCalculator import calculate_fragment_occurrence_probabilities
from Graph import Graph
from Read import Read
from ReadPair import ReadPair
from ToDeBruijnGraph import to_debruijn_graph
from Utils import generate_random_genome, count_kmers

T = TypeVar('T', Read, ReadPair)


# MARKDOWN
def pair_reverse_complements(occurrence_probabilities: Dict[T, float]) -> Tuple[List[Tuple[T, T]], List[T]]:
    rc_pairs = []
    unpairables = []
    for frag in occurrence_probabilities:
        rc_frag = frag.reverse_complement()
        if rc_frag == frag:
            unpairables.append(frag)
        elif frag not in occurrence_probabilities\
                or rc_frag not in occurrence_probabilities:
            unpairables.append(frag)
        elif occurrence_probabilities[frag] != occurrence_probabilities[rc_frag]:
            unpairables.append(frag)
        else:
            rc_pairs.append((frag, rc_frag))
    return rc_pairs, unpairables
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        lines = []
        while True:
            try:
                line = input().strip()
                if len(line) > 0:
                    lines.append(line)
            except EOFError:
                break

        occurrence_probabilities = dict([(Read(l.split()[0]), float(l.split()[1])) for l in lines])
        print(f'Probability of occurrence in genome:', end='\n\n')
        for read, appearances in occurrence_probabilities.items():
            print(f' * {read} probably has {appearances} appearances in the genome.')
        paired_complements, unpairables = pair_reverse_complements(occurrence_probabilities)
        print(f'', end='\n\n')
        print(f'Paired reverse complementing fragments:', end='\n\n')
        for read1, read2 in paired_complements:
            print(f' * {read1} / {read2}')
        print(f'', end='\n\n')
        print(f'Unpairable fragments:', end='\n\n')
        for read1 in unpairables:
            print(f' * {read1}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
