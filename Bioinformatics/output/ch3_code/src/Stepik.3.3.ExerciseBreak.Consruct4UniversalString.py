from Kmer_ToOverlapGraphHash import to_overlap_graph
from Kmer_StringSpelledByGenomePath import string_spelled_by_genome_path
from Utils import enumerate_patterns

segments = list(enumerate_patterns(4, '01'))
print(f'{segments}')

nodes = to_overlap_graph(segments)
for kmer, other_kmers in sorted(nodes.items()):
    print(f'{kmer} -> {",".join(other_kmers)}')

def walk(path):
    if len(path) == len(nodes):
        print(f'{path} -> {string_spelled_by_genome_path(path)}')
        return

    n = path[-1]
    for child_n in nodes[n]:
        if child_n not in path:
            path.append(child_n)
            walk(path)
            path.pop()


for node in nodes.keys():
    walk([node])