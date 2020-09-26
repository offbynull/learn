from EulerianPathToEulerianCycle import find_eularian_path_in_nearly_balanced_graph, \
    normalize_graph_representation

with open('/home/user/Downloads/dataset_240261_6.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
adjacency_list = lines[:]
adjacency_list = [l.strip() for l in adjacency_list] # get rid of whitespace
adjacency_list = [l for l in adjacency_list if len(l) > 0] # get rid of empty lines
adjacency_list = [l.split(' -> ') for l in adjacency_list]
adjacency_list = [(l[0], l[1].split(',')) for l in adjacency_list]

graph = dict(adjacency_list)
normalize_graph_representation(graph)

path = find_eularian_path_in_nearly_balanced_graph(graph)
print(f'{"->".join(path)}')