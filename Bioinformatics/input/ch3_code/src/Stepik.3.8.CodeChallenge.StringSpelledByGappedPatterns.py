from Kdmer_StringSpelledByGenomePath import string_spelled_by_genome_path

with open('/home/user/Downloads/dataset_240266_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()


lines = data.split('\n')
lines = [l.strip() for l in lines]  # get rid of whitespace
lines = [l for l in lines if len(l) > 0]  # get rid of empty li
k, d = [int(s) for s in lines[0].split(' ')]
kdmers = [tuple(s.split('|', maxsplit=2)) for s in lines[1:]]

kdmers = [(k1, k2) for k1, k2 in kdmers]  # silence warning, without this assumed type of kdmers is List[Tuple[str, ...]] where the func its passed to expects be List[Tuple[str,str]]

genome = string_spelled_by_genome_path(kdmers, d)
print(f'{genome}')