from Kmer_StringSpelledByGenomePath import string_spelled_by_genome_path

with open('/home/user/Downloads/dataset_240256_3(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
dnas = lines[:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

composition = string_spelled_by_genome_path(dnas)
print(composition)