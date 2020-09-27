from Kmer_ToOverlapGraphHash import to_overlap_graph

with open('/home/user/Downloads/dataset_240256_10(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
dnas = lines[:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

overlaps = to_overlap_graph(dnas)
for kmer, other_kmers in overlaps.items():
    if len(other_kmers) == 0:
        continue
    print(f'{kmer} -> {",".join(other_kmers)}')
