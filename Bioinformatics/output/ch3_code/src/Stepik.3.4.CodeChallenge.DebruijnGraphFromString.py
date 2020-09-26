from Kmer_ToDeBruijnGraph import to_debruijn_graph_from_genome_path

with open('/home/user/Downloads/dataset_240257_6.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0].strip())
dna = lines[1].strip()

nodes = to_debruijn_graph_from_genome_path(k, dna)
for node, other_nodes in nodes.items():
    if len(other_nodes) == 0:
        continue
    print(f'{node} -> {",".join(other_nodes)}')