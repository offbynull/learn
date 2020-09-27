from Kmer_ToDeBruijnGraph import to_debruijn_graph

with open('/home/user/Downloads/dataset_240258_8(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmers = lines[:]
kmers = [l.strip() for l in kmers] # get rid of whitespace
kmers = [l for l in kmers if len(l) > 0] # get rid of empty lines

nodes = to_debruijn_graph(kmers)
for node, other_nodes in nodes.items():
    if len(other_nodes) == 0:
        continue
    print(f'{node} -> {",".join(other_nodes.elements())}')