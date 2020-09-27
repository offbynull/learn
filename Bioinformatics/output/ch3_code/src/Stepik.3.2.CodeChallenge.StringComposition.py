from Kmer_StringComposition import string_composition

with open('/home/user/Downloads/dataset_240255_3(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0])
text = lines[1]

composition = string_composition(k, text)
print('\n'.join(composition))