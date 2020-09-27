from collections import Counter

from Utils import normalize_graph
from WalkEulerianCycle import walk_eularian_cycle

with open('/home/user/Downloads/dataset_240261_2(2).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
adjacency_list = lines[:]
adjacency_list = [l.strip() for l in adjacency_list] # get rid of whitespace
adjacency_list = [l for l in adjacency_list if len(l) > 0] # get rid of empty lines
adjacency_list = [l.split(' -> ') for l in adjacency_list]
adjacency_list = [(l[0], Counter(l[1].split(','))) for l in adjacency_list]

graph = dict(adjacency_list)
normalize_graph(graph)

cycle_path = walk_eularian_cycle(graph, next(iter(graph.keys())))
print(f'{"->".join(cycle_path)}')