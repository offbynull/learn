from BruteforceOverlapSearch import bruteforce_find_overlaps

with open('/home/user/Downloads/dataset_240256_10.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
dnas = lines[:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

overlaps = bruteforce_find_overlaps(dnas)
for kmer, other_kmers in overlaps.items():
    print(f'{kmer} -> {",".join(other_kmers)}')
