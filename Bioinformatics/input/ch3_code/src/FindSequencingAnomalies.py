from collections import Counter
from random import Random
from typing import Dict, List, TypeVar, Optional, Tuple

from Graph import Graph
from Read import Read
from ReadPair import ReadPair
from ToDeBruijnGraph import to_debruijn_graph
from Utils import generate_random_genome, count_kmers

T = TypeVar('T', Read, ReadPair)


# If less than 50% of the reads are from repeats, this attempts to count and normalize such that it can hint at which
# reads may contain errors (= ~0) and which reads are for repeat regions (> 1.0).
def normalize_based_on_read_counts(reads: List[T]) -> Dict[T, float]:
    counter = Counter(reads)
    max_digit_count = max([len(str(count)) for count in counter.values()])
    for i in range(max_digit_count):
        rounded_counter = Counter(dict([(k, round(count, -i)) for k, count in counter.items()]))
        for k, orig_count in counter.items():
            if rounded_counter[k] == 0:
                rounded_counter[k] = orig_count
        most_occurring_count, times_counted = Counter(rounded_counter.values()).most_common(1)[0]
        if times_counted >= len(rounded_counter) * 0.5:
            return dict([(key, value / most_occurring_count) for key, value in rounded_counter.items()])
    raise ValueError('Failed to find a common count')


def walk_outs_until_converge(graph: Graph[T], node: T) -> Optional[List[T]]:
    ret = [node]
    ret_quick_lookup = {node}
    while True:
        in_degree = graph.get_in_degree(node)
        if in_degree > 1:
            return ret

        children = graph.get_outputs(node)
        child = next(children, None)
        if child is None or child in ret_quick_lookup:
            return None

        node = child
        ret.append(node)
        ret_quick_lookup.add(node)


def walk_ins_until_diverge(graph: Graph[T], node: T) -> Optional[List[T]]:
    ret = [node]
    ret_quick_lookup = {node}
    while True:
        in_degree = graph.get_out_degree(node)
        if in_degree > 1:
            return ret

        parents = graph.get_inputs(node)
        parent = next(parents, None)
        if parent is None or parent in ret_quick_lookup:
            return None

        node = parent
        ret.insert(0, node)
        ret_quick_lookup.add(node)


def find_head_convergences(graph: Graph[T], branch_len: int) -> List[Tuple[Optional[T], List[T], Optional[T]]]:
    root_nodes = filter(lambda n: graph.get_in_degree(n) == 0, graph.get_nodes())

    ret = []
    for n in root_nodes:
        for child in graph.get_outputs(n):
            path_from_child = walk_outs_until_converge(graph, child)
            if path_from_child is None:
                continue
            diverging_node = None
            branch_path = [n] + path_from_child[:-1]
            converging_node = path_from_child[-1]
            path = (diverging_node, branch_path, converging_node)
            if len(branch_path) <= branch_len:
                ret.append(path)
    return ret


def find_tail_divergences(graph: Graph[T], branch_len: int) -> List[Tuple[Optional[T], List[T], Optional[T]]]:
    tail_nodes = filter(lambda n: graph.get_out_degree(n) == 0, graph.get_nodes())

    ret = []
    for n in tail_nodes:
        for child in graph.get_inputs(n):
            path_from_child = walk_ins_until_diverge(graph, child)
            if path_from_child is None:
                continue
            diverging_node = path_from_child[0]
            branch_path = path_from_child[1:] + [n]
            converging_node = None
            path = (diverging_node, branch_path, converging_node)
            if len(branch_path) <= branch_len:
                ret.append(path)
    return ret


def find_bubbles(graph: Graph[T], branch_len: int) -> List[Tuple[Optional[T], List[T], Optional[T]]]:
    branching_nodes = filter(lambda n: graph.get_out_degree(n) > 1, graph.get_nodes())

    ret = []
    for n in branching_nodes:
        for child in graph.get_outputs(n):
            path_from_child = walk_outs_until_converge(graph, child)
            if path_from_child is None:
                continue
            diverging_node = n
            branch_path = path_from_child[:-1]
            converging_node = path_from_child[-1]
            path = (diverging_node, branch_path, converging_node)
            if len(branch_path) <= branch_len:
                ret.append(path)
    return ret


def to_graphviz(graph: Graph, weights: Dict[T, float]) -> str:
    out = ''
    for node in graph.get_nodes():
        for to_node in graph.get_outputs(node):
            read = node.append_overlap(to_node)
            weight = weights[read]
            r = 0
            g = 0
            b = 0
            if weight < 1.0:
                r = int(255 * (1.0 - weight))
            elif weight > 1.0:
                r = int(255 * (max(weight - 1.0, 1.0)))
                b = r
            color = '#' + format(r, '02x') + format(g, '02x') + format(b, '02x')
            out += '"' + str(node).replace("\"", "\\\"") + '\"'\
                   + ' -> '\
                   + '"' + str(to_node).replace("\"", "\\\"") + '"'\
                   + f' [color="{color}"];\n'
    # https://stackoverflow.com/questions/8610710/compacting-a-digraph-in-graphviz-using-dot-language
    return 'digraph {\n'\
           + 'graph[center=true, margin=0.2, nodesep=0.1, ranksep=0.15]\n'\
           + 'node[shape=none, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'\
           + 'edge[arrowsize=0.6, arrowhead=vee]\n'\
           + out\
           + '}\n'


if __name__ == '__main__':
    r = Random(126)

    genome_len = 50
    k_read = 12
    k_break = 6

    genome = generate_random_genome(genome_len, r=r)
    reads = Read.random_fragment(genome, k_read, count_kmers(genome_len, k_read) * 30, r=r)
    reads[0] = reads[0].introduce_random_errors(1, r=r)
    reads = [broken_read for read in reads for broken_read in read.shatter(k_break)]
    normalized_read_counts = normalize_based_on_read_counts(reads)
    print(f'{normalized_read_counts}')
    reads = reads[0].collapse(reads)
    graph = to_debruijn_graph(reads)
    print(to_graphviz(graph, normalized_read_counts))
    potentially_bad_paths = find_bubbles(graph, k_break)\
                            + find_head_convergences(graph, k_break)\
                            + find_tail_divergences(graph, k_break)
    for src, branch, dst in potentially_bad_paths:
        print(f'Src: {src}, Dst: {dst}, Branch: {"->".join([str(x) for x in branch])}')
