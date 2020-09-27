from Kmer_ToDeBruijnGraph import to_debruijn_graph
from Utils import enumerate_patterns
from WalkEulerianCycle import walk_eularian_cycle

with open('/home/user/Downloads/dataset_240261_11(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0])

kmers = list(enumerate_patterns(k, '01'))
graph = to_debruijn_graph(kmers)
path = walk_eularian_cycle(graph, next(iter(graph.keys())))
str = ''.join(path[0:1] + [e[-1] for e in path[1:]])
str = str[:-(k - 1)]
print(str)