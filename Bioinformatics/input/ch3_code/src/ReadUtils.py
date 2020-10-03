from __future__ import annotations

import random
from typing import Tuple, List

from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair


def generate_random_genome(size: int) -> str:
    return ''.join([random.choice(['A', 'C', 'T', 'G']) for i in range(size)])


def generate_random_reads(data: str, k: int, read_count: int) -> List[Read]:
    total_kmers = len(data) - k + 1
    ret = []
    for i in range(read_count):
        offset = random.randint(0, total_kmers)
        kmer = data[offset:offset+k]
        read = Read(kmer)
        ret.append(read)
    return ret


def generate_random_read_pairs(data: str, k: int, d: int, read_count: int) -> List[ReadPair]:
    total_kmers = len(data) - (k*2 + d) + 1
    ret = []
    for i in range(read_count):
        offset = random.randint(0, total_kmers)
        kdmer_head = data[offset:offset+k]
        kdmer_tail = data[offset+k+d:offset+k+d+k]
        kdmer = Kdmer(kdmer_head, kdmer_tail, d)
        read = ReadPair(kdmer)
        ret.append(read)
    return ret



def introduce_random_errors_in_read(read: Read, count: int) -> Read:
    data = read.data
    offsets = list(range(len(data)))
    for i in range(count):
        offset = random.choice(offsets)
        offsets.remove(offset)
        choices = ['A', 'C', 'T', 'G']
        choices.remove(data[offset])
        data = data[:offset] + random.choice(choices) + data[offset+1:]
    return Read(data, source=read)


def introduce_random_errors_in_read_pair(read_pair: ReadPair, count: int) -> ReadPair:
    data = read_pair.data.head + read_pair.data.tail
    offsets = list(range(len(data)))
    for i in range(count):
        offset = random.choice(offsets)
        offsets.remove(offset)
        choices = ['A', 'C', 'T', 'G']
        choices.remove(data[offset])
        data = data[:offset] + random.choice(choices) + data[offset+1:]
    return ReadPair(Kdmer(data[:read_pair.k], data[read_pair.k:], read_pair.d), source=read_pair)
