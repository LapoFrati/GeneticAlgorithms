import pprint
import string
import random
import numpy as np
pp = pprint.PrettyPrinter()
amleto = 'parmi somigli ad una donnola'
valutazioni = 0


def random_char():
    return random.choice(string.ascii_lowercase + ' ')


def valuta(candidato):
    global valutazioni
    valutazioni = valutazioni + 1
    azzeccate = 0
    for (lettera1, lettera2) in zip(candidato, amleto):
        if lettera1 == lettera2:
            azzeccate = azzeccate + 1
    return azzeccate


def altera(vecchia_frase):
    posizione_da_cambiare = random.choice(range(0, len(vecchia_frase)))
    lettera_da_cambiare = vecchia_frase[posizione_da_cambiare]
    alternative = (string.ascii_lowercase +
                   ' ').replace(lettera_da_cambiare, '')
    nuova_frase = list(vecchia_frase)
    nuova_frase[posizione_da_cambiare] = random.choice(alternative)
    return nuova_frase


def altera2(vecchia_frase):
    mutation_rate = 2. / len(vecchia_frase)
    nuova_frase = []
    for letter in vecchia_frase:
        if random.random() < mutation_rate:
            nuova_frase.append(random.choice(
                (string.ascii_lowercase + ' ').replace(letter, "")))
        else:
            nuova_frase.append(letter)
    return nuova_frase


def hillclimber(stampa=False):
    i = 0
    global valutazioni
    valutazioni = 0
    miglior_frase = [random_char() for n in range(0, len(amleto))]
    miglior_risultato = valuta(miglior_frase)
    while(miglior_risultato < len(amleto)):
        frase = altera(miglior_frase)
        risposta = valuta(frase)
        i = i + 1
        if risposta > miglior_risultato:
            miglior_risultato = risposta
            miglior_frase = frase
            if stampa:
                print(str(i) + ':\t"' + ''.join(miglior_frase) +
                      '"\t' + str(miglior_risultato))
    return valutazioni


def stampa_candidati(candidati):
    # candidati -> array di char, li trasformo in stringhe con ''.join(...)
    # [' ', 'x', 'p', 'l', 'f', … ,'d', 'z', 'h', 'f'] -> ' xplfrvvjjvnmzkovohltroudzhf'
    stringhe_e_valori = list(map(lambda x: (''.join(x[0]), x[1]), candidati))
    # per comodità ordino le stringhe in base al numero di lettere corrette, decrescente
    stringhe_ordinate = sorted(
        stringhe_e_valori, key=lambda tup: tup[1], reverse=True)
    pp.pprint(stringhe_ordinate)


def mescola(frase1, frase2):
    nuova_frase = []
    for i in range(0, len(frase1[0])):
        if random.random() > 0.5:
            nuova_frase.append(frase1[0][i])
        else:
            nuova_frase.append(frase2[0][i])
    return (nuova_frase, valuta(nuova_frase))


def genera_ruota(candidati):
    totale = 0
    ruota = []
    for frase, valore in candidati:
        totale = totale + valore
        ruota.append((totale, frase, valore))
    return ruota


def gira_ruota(wheel):
    totale = wheel[-1][0]
    pick = totale * random.random()
    for (parziale, candidato, valore) in wheel:
        if parziale >= pick:
            return (candidato, valore)
    return random.choice(wheel)[1:]


def migliore(candidati):
    ordinati = sorted(candidati, key=lambda tup: tup[1], reverse=True)
    return ordinati[0]


def prova_piu_frasi_e_mescola(num_frasi, stampa=False):
    candidati = []
    global valutazioni
    valutazioni = 0
    for i in range(0, num_frasi):
        tmp_frase = [random_char() for n in range(0, len(amleto))]
        tmp_risposta = valuta(tmp_frase)
        candidati.append((tmp_frase, tmp_risposta))
    i = 0
    miglior_frase = [random_char() for n in range(0, len(amleto))]
    miglior_risultato = valuta(miglior_frase)
    while(miglior_risultato < len(amleto)):
        i = i + 1
        ruota = genera_ruota(candidati)
        nuovi_candidati = []
        for n in range(0, len(candidati)):
            minitorneo = [gira_ruota(ruota), gira_ruota(ruota)]
            nuova_frase = altera(mescola(minitorneo[0], minitorneo[1])[0])
            nuova_risposta = valuta(nuova_frase)
            minitorneo.append((nuova_frase, nuova_risposta))
            vincitore, valore_vincitore = migliore(minitorneo)
            nuovi_candidati.append((vincitore, valore_vincitore))
            if valore_vincitore > miglior_risultato:
                miglior_risultato = valore_vincitore
                miglior_frase = vincitore
                if stampa:
                    print(str(i) + ':\t"' + ''.join(miglior_frase) +
                          '"\t' + str(miglior_risultato))
                    stampa_candidati(candidati)
        candidati = nuovi_candidati
    return valutazioni


def prova_piu_frasi_insieme(num_frasi, stampa=False):
    candidati = []
    global valutazioni
    valutazioni = 0
    for i in range(0, num_frasi):
        tmp_frase = [random_char() for n in range(0, len(amleto))]
        tmp_risposta = valuta(tmp_frase)
        candidati.append((tmp_frase, tmp_risposta))
    i = 0
    miglior_frase = [random_char() for n in range(0, len(amleto))]
    miglior_risultato = valuta(miglior_frase)
    while(miglior_risultato < len(amleto)):
        i = i + 1
        for n in range(0, len(candidati)):
            frase, risposta = candidati[n]
            nuova_frase = altera(frase)
            nuova_risposta = valuta(nuova_frase)
            if nuova_risposta > risposta:
                candidati[n] = (nuova_frase, nuova_risposta)
            if nuova_risposta > miglior_risultato:
                miglior_risultato = nuova_risposta
                miglior_frase = nuova_frase
                if stampa:
                    print(str(i) + ':\t"' + ''.join(miglior_frase) +
                          '"\t' + str(miglior_risultato))
    return valutazioni


def test_hill(runs=20):
    results = []
    for i in range(0, runs):
        results.append(hillclimber())
    return np.average(results), np.std(results)


def test_others(function_to_test, pop_size=100, runs=20)
    results = []
    for i in range(0, runs):
        results.append(function_to_test(pop_size))
    return np.average(results), np.std(results)


def main():
    print(test(hillclimber, 50))
    print(test_others(prova_piu_frasi_e_mescola, runs=50))


if __name__ == '__main__':
    main()
