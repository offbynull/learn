from typing import Dict, List, TypeVar, Optional, Tuple

from Graph import Graph
from Read import Read
from ToDeBruijnGraph import to_debruijn_graph

T = TypeVar('T')


def walk_until_converge(graph: Graph[T], node: T) -> Optional[List[T]]:
    ret = [node]
    while True:
        in_degree = graph.get_in_degree(node)
        if in_degree > 1:
            return ret

        children = graph.get_outputs(node)
        child = next(children)
        if child in ret:
            return None

        node = child
        ret.append(node)


# bubbles that have lower coverage are probably from faulty reads, and probably should be discarded
def find_bubbles(graph: Graph[T], k: int) -> Dict[Tuple[T, T], List[List[T]]]:
    branching_nodes = filter(lambda n: graph.get_out_degree(n) > 1, graph.get_nodes())

    ret = dict()
    for n in branching_nodes:
        potential_bubbles = []
        for child in graph.get_outputs(n):
            # walk until converge...
            path_from_child = walk_until_converge(graph, child)
            path = [n] + path_from_child
            # if number of nodes walked corresponds to the size of a read...
            #   len(path)-2 because start and end are the branching/converging nodes
            #   k-1 because nodes in de bruijn graph represent (k-1)mers
            if len(path)-2 <= k-1:
                potential_bubbles.append(path)
        # group bubble paths by same start node and same end node
        head_tail_set = set([(x[0], x[-1]) for x in potential_bubbles])
        for head, tail in head_tail_set:
            matching_path = list(filter(lambda x: x[0] == head and x[-1] == tail, potential_bubbles))
            ret.setdefault((head, tail), []).extend(matching_path)
    return ret


if __name__ == '__main__':
    # random.seed(1)
    # data = generate_random_genome(60)
    # reads = generate_random_reads(data, 12, 60 * 100)
    # error_read = reads[0]
    # error_read = introduce_random_errors_in_read(error_read, 1)
    # reads[0] = error_read
    # reads = [broken_read for read in reads for broken_read in read.shatter(7)]
    # graph = to_debruijn_graph(set(reads))
    # print(graph.to_graphviz())
    graph = to_debruijn_graph([
        Read('CCGTA'),
        Read('CGTAT'),
        Read('GTATG'),
        Read('TATGG'),
        Read('ATGGA'),
        Read('TGGAC'),
        Read('GGACA'),
        Read('CGTAC'),
        Read('GTACG'),
        Read('TACGG'),
        Read('ACGGA'),
        Read('CGGAC')
    ])
    found = find_bubbles(graph, 5)
    for bounds, paths in found.items():
        for path in paths:
            print(f'{bounds} = {"->".join([str(x) for x in path])}')
