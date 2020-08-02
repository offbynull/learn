from MotifEntropy import motify_entropy

if __name__ == '__main__':
    entropy = motify_entropy([
        'TCGGGGgTTTtt'.lower(),
        'cCGGtGAcTTaC'.lower(),
        'aCGGGGATTTtC'.lower(),
        'TtGGGGAcTTtt'.lower(),
        'aaGGGGAcTTCC'.lower(),
        'TtGGGGAcTTCC'.lower(),
        'TCGGGGATTcat'.lower(),
        'TCGGGGATTcCt'.lower(),
        'TaGGGGAacTaC'.lower(),
        'TCGGGtATaaCC'.lower()
    ])

    print(f'{entropy}')