from EulerianPathToEulerianCycle import normalize_graph_representation, \
    find_eularian_path_in_nearly_balanced_graph
from Kmer_StringSpelledByGenomePath import string_spelled_by_genome_path
from Kmer_ToDeBruijnGraph import to_debruijn_graph

with open('/home/user/Downloads/dataset_240261_7.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0].strip())
kmers = lines[1:]
kmers = [l.strip() for l in kmers] # get rid of whitespace
kmers = [l for l in kmers if len(l) > 0] # get rid of empty lines

graph = to_debruijn_graph(kmers)
normalize_graph_representation(graph)

path = find_eularian_path_in_nearly_balanced_graph(graph)
genome = string_spelled_by_genome_path(path)
print(f'{genome}')