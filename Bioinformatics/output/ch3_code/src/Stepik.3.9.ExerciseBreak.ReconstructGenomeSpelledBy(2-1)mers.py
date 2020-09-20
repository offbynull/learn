from Kdmer import Kdmer
from Kdmer_StringSpelledByGenomePath import string_spelled_by_genome_path


# AG-AG
#  GC-GC
#   CA-CT
#    AG-TG
#     GC-GC
#      CT-CT
#       TG-TG
#        GC-GC
#         CT-CA
# AGCAGCTGCTGCA
out = string_spelled_by_genome_path([
    Kdmer('AG', 'AG', 1),
    Kdmer('GC', 'GC', 1),
    Kdmer('CA', 'CT', 1),
    Kdmer('AG', 'TG', 1),
    Kdmer('GC', 'GC', 1),
    Kdmer('CT', 'CT', 1),
    Kdmer('TG', 'TG', 1),
    Kdmer('GC', 'GC', 1),
    Kdmer('CT', 'CA', 1)
])
print(f'{out}')
