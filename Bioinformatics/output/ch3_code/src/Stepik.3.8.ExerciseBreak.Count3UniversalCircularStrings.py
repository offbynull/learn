from collections import Counter
from typing import List

from Kmer_StringSpelledByGenomePath import string_spelled_by_genome_path
from Utils import normalize_graph
from WalkEulerianCycle import walk_eularian_cycle

adjacency_list = [
    ('00', Counter(['00', '01'])),
    ('01', Counter(['10', '11'])),
    ('10', Counter(['00', '01'])),
    ('11', Counter(['10', '11'])),
]
graph = dict(adjacency_list)
graph = normalize_graph(graph)


def prefix(kmer: str):
    return kmer[:-1]


def suffix(kmer: str):
    return kmer[1:]


def eularian_path_to_kmers(cycle_path: List[str]) -> List[str]:
    out = []
    for i in range(len(cycle_path) - 1):
        out.append(cycle_path[i] + cycle_path[i+1][-1])
    return out


def do_kmers_cycle(kmers: List[str]) -> bool:
    for i in range(len(kmers) - 1):
        if suffix(kmers[i]) != prefix(kmers[i+1]):
            return False
    if suffix(kmers[-1]) != prefix(kmers[0]):
        return False
    return True


cycle_path = walk_eularian_cycle(graph, '00')
print(f'{eularian_path_to_kmers(cycle_path)}')
print(f'{string_spelled_by_genome_path(eularian_path_to_kmers(cycle_path))}')
print(f'{do_kmers_cycle(eularian_path_to_kmers(cycle_path))}')
cycle_path = walk_eularian_cycle(graph, '01')
print(f'{eularian_path_to_kmers(cycle_path)}')
print(f'{string_spelled_by_genome_path(eularian_path_to_kmers(cycle_path))}')
print(f'{do_kmers_cycle(eularian_path_to_kmers(cycle_path))}')
cycle_path = walk_eularian_cycle(graph, '10')
print(f'{eularian_path_to_kmers(cycle_path)}')
print(f'{string_spelled_by_genome_path(eularian_path_to_kmers(cycle_path))}')
print(f'{do_kmers_cycle(eularian_path_to_kmers(cycle_path))}')
cycle_path = walk_eularian_cycle(graph, '11')
print(f'{eularian_path_to_kmers(cycle_path)}')
print(f'{string_spelled_by_genome_path(eularian_path_to_kmers(cycle_path))}')
print(f'{do_kmers_cycle(eularian_path_to_kmers(cycle_path))}')

# ['000', '001', '011', '111', '110', '101', '010', '100']
# 0001110100
# True
# ['011', '111', '110', '100', '000', '001', '010', '101']
# 0111000101
# True
# ['100', '000', '001', '010', '101', '011', '111', '110']
# 1000101110
# True
# ['110', '100', '000', '001', '010', '101', '011', '111']
# 1100010111
# True

# The website says accepts the answer of 2, but clearly this is showing that hte answer is 4? starting from each node
# [00, 01, 10, 11], the string that gets generated is always circular -- each kmer appears exactly once and is ordered
# in such a way that it's circular.

# All 4 strings above are just shifted versions of the same string. Maybe what 2 means is that 1 string is the one
# calculated in the code above, and the other string is the reverse of the string? or the complement of that string?

