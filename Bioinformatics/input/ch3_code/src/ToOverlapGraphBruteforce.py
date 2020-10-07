from typing import List, TypeVar

from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair

T = TypeVar('T', Read, ReadPair)


# MARKDOWN
def to_overlap_graph(items: List[T], skip: int = 1) -> Graph[T]:
    ret = Graph()
    for i, item in enumerate(items):
        for j, other_item in enumerate(items):
            if i == j:
                continue
            if item.suffix(skip) == other_item.prefix(skip):
                ret.insert_edge(item, other_item)
    return ret
# MARKDOWN


# if __name__ == '__main__':
#     out = to_overlap_graph([
#         Read('ATGCG'),
#         Read('GCATG'),
#         Read('CATGC'),
#         Read('AGGCA'),
#         Read('GGCAT'),
#         Read('GGCAC')
#     ])
#     print(f'{out}')
#
#     out = to_overlap_graph([
#         ReadPair(Kdmer('AT', 'CG', 1)),
#         ReadPair(Kdmer('GC', 'TG', 1)),
#         ReadPair(Kdmer('CA', 'GC', 1)),
#         ReadPair(Kdmer('AG', 'CA', 1)),
#         ReadPair(Kdmer('GG', 'AT', 1)),
#         ReadPair(Kdmer('GG', 'AC', 1))
#     ])
#     print(f'{out}')

def to_graphviz(g: Graph) -> str:
    out = ''
    for node, to_nodes in g._outbound.items():
        for to_node in to_nodes.elements():
            from_node_str = str(node) + ' [' + str(node.instance) + ']'
            to_node_str = str(to_node) + ' [' + str(to_node.instance) + ']'
            out += '"' + from_node_str.replace("\"", "\\\"") + '\"'\
                   + ' -> '\
                   + '"' + to_node_str.replace("\"", "\\\"") + '"'\
                   + ' [shape=plain];\n'
    return 'digraph {\n'\
           + 'graph[center=true, margin=0.2, nodesep=0.2, ranksep=0.2]\n'\
           + 'node[shape=rectangle, fontname="Courier-Bold", fontsize=10, fixedsize=true]\n'\
           + 'edge[arrowsize=0.6, arrowhead=vee]\n'\
           + out\
           + '}\n'

def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        lines = []
        while True:
            try:
                line = input().strip()
                if len(line) > 0:
                    lines.append(line)
            except EOFError:
                break

        command = lines[0]
        lines = lines[1:]
        if command == 'reads':
            reads = [Read(l, i) for i, l in enumerate(lines)]
            graph = to_overlap_graph(reads)
        elif command == 'read-pairs':
            read_pairs = [ReadPair(Kdmer(l.split('|')[0], l.split('|')[2], int(l.split('|')[1])), i) for i, l in enumerate(lines)]
            graph = to_overlap_graph(read_pairs)
        else:
            raise
        print(f'Given the fragments {lines}, the overlap graph is...', end="\n\n")
        print(f'```{{dot}}\n{to_graphviz(graph)}\n```\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()