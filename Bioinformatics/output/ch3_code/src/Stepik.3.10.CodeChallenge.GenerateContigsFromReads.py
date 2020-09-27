from FindMaximalNonBranchingPaths import find_maximal_non_branching_paths
from Kmer_StringSpelledByGenomePath import string_spelled_by_genome_path
from Kmer_ToDeBruijnGraph import to_debruijn_graph

with open('/home/user/Downloads/dataset_240263_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmers = lines[:]
kmers = [l.strip() for l in kmers] # get rid of whitespace
kmers = [l for l in kmers if len(l) > 0] # get rid of empty lines

graph = to_debruijn_graph(kmers)
contigs = find_maximal_non_branching_paths(graph)
for contig in contigs:
    output = string_spelled_by_genome_path(contig)
    print(f'{output}')