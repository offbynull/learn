from Utils import slide_window

dna = 'TAATGCCATGGGATGTT'
kdmers = []
for a, b in zip(slide_window(dna, 3), slide_window(dna[5:], 3)):
    kdmers.append('(' + a[0] + '|' + b[0] + ')')

kdmers.sort()
print(f'{" ".join(kdmers)}')