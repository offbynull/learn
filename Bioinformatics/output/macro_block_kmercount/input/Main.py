dna_seq = input()
kmer = input()

k = len(kmer)
idxes = []
for i in range(0, len(dna_seq) - k):
    if dna_seq[i:i+k] == kmer:
        idxes.append(i)
print(f'{idxes}')