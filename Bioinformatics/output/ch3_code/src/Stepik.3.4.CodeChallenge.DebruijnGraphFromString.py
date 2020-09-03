from DeBruijnGraphFromString import debruijn_graph_from_string

with open('/home/user/Downloads/dataset_240257_6.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0].strip())
dna = lines[1].strip()

nodes = debruijn_graph_from_string(k, dna)
for node, other_nodes in nodes.items():
    print(f'{node} -> {",".join(other_nodes)}')