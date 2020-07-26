from DistanceBetweenPatternAndStrings import distance_between_pattern_and_strings
from MedianString import median_string
from MotifEnumeration import motif_enumeration

with open('/home/user/Downloads/dataset_240240_9.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0])
dnas = lines[1:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

dist = median_string(k, dnas)
print(f'{dist[0]}')