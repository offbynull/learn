from DeBruijnGraphFromKmers import debruijn_graph_from_kmers
from EulerianCycle import eularian_cycle
from Utils import enumerate_patterns

with open('/home/user/Downloads/dataset_240261_11.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0])

kmers = list(enumerate_patterns(k, '01'))
graph = debruijn_graph_from_kmers(kmers)
path = eularian_cycle(graph)
str = ''.join(path[0:1] + [e[-1] for e in path[1:]])
str = str[:-(k - 1)]
print(str)