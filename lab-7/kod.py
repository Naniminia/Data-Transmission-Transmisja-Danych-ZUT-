import numpy as np
import matplotlib.pyplot as plt
import math
import cmath

# zad 1
x = [1, 1, 0, 1]
string1 = 'd'


def zamiana(string1):
    string3 = ''
    for i in string1:
        string3 += bin(ord(i))[2:].zfill(8)
    return string3


string2 = zamiana(string1)
Tb = 1
W = 2
fn = W * pow(Tb, -1)
fs = 200
Tc = (Tb * len(string2)) + 1 / fs
fi = 180
f = 1000
N = int(Tc * fs)
fn1 = (W + 1) / Tb
fn2 = (W + 2) / Tb


def HammingKoder(x):
    x_len = len(x)
    num_bits = ((x_len + 3) // 4) * 7  # Upewnij się, że jest wielokrotnością 4 i 7
    x1 = np.zeros(num_bits, int)

    for i in range(x_len // 4):  # Pętla powinna iterować po blokach 4-bitowych
        x1[i * 7 + 2] = x[i * 4]
        x1[i * 7 + 4] = x[i * 4 + 1]
        x1[i * 7 + 5] = x[i * 4 + 2]
        x1[i * 7 + 6] = x[i * 4 + 3]

        # Obliczanie bitów parzystości
        a = ((x1[i * 7 + 2] + x1[i * 7 + 4] + x1[i * 7 + 6]) % 2)
        b = ((x1[i * 7 + 2] + x1[i * 7 + 5] + x1[i * 7 + 6]) % 2)
        c = ((x1[i * 7 + 4] + x1[i * 7 + 5] + x1[i * 7 + 6]) % 2)

        # Przypisywanie bitów parzystości
        x1[i * 7] = a
        x1[i * 7 + 1] = b
        x1[i * 7 + 3] = c

    return x1


def HammingDekoder(x1):
    x1_len = len(x1)
    num_bits = (x1_len // 7) * 4  # Liczba bitów wejściowych
    x2 = np.zeros(num_bits, int)

    for i in range(x1_len // 7):
        x2[i * 4] = x1[i * 7 + 2]
        x2[i * 4 + 1] = x1[i * 7 + 4]
        x2[i * 4 + 2] = x1[i * 7 + 5]
        x2[i * 4 + 3] = x1[i * 7 + 6]

    # Liczenie syndromu
    syndromes = []
    for i in range(x1_len // 7):
        x1prim = (x1[i * 7] + x1[i * 7 + 2] + x1[i * 7 + 4] + x1[i * 7 + 6]) % 2
        x1prim2 = (x1[i * 7 + 1] + x1[i * 7 + 2] + x1[i * 7 + 5] + x1[i * 7 + 6]) % 2
        x1prim4 = (x1[i * 7 + 3] + x1[i * 7 + 4] + x1[i * 7 + 5] + x1[i * 7 + 6]) % 2

        S = (x1prim * pow(2, 0)) + (x1prim2 * pow(2, 1)) + (x1prim4 * pow(2, 2))
        syndromes.append(S)

    return x2, syndromes


def modulacjaPSK(string2):
    def KluczowaniePSK(string2, A1, A2, fn, fs, Tb):
        wyjsciePSK1 = []
        wyjsciePSK2 = []
        for n in range(0, N - 1):
            t = n / fs
            indeks = int(t / Tb)
            wyjsciePSK1.append(t)

            if string2[indeks] == '0':
                wyjsciePSK2.append(math.sin(2 * math.pi * fn * t))
            else:
                wyjsciePSK2.append(math.sin(2 * math.pi * fn * t + math.pi))
        return wyjsciePSK1, wyjsciePSK2

    A1 = 1
    A2 = 2
    x_PSK, y_PSK = KluczowaniePSK(string2, A1, A2, fn, fs, Tb)
    return x_PSK, y_PSK


def demodulacjaPSK(x_PSK, y_PSK):
    def PSK_xt(y_PSK, fn, fs):
        wyjscie = []
        for n in range(len(y_PSK)):
            t = n / fs
            wyjscie.append(y_PSK[n] * (np.sin(2 * np.pi * fn * t)))
        return wyjscie

    wartosci_XT = PSK_xt(y_PSK, fn, fs)

    def PSK_pt(wartosci_XT, N, fs):
        dt = 1 / fs
        calka = []
        for i in range(0, len(wartosci_XT), N):
            calka_bit = []
            suma = 0
            for j in range(N):
                if i + j < len(wartosci_XT):
                    suma += wartosci_XT[i + j] * dt
                    calka_bit.append(suma)
            calka.extend(calka_bit)
        return calka

    wartosci_pt = PSK_pt(wartosci_XT, N, fs)

    wartosc_progu = 0.01

    def PSK_ct(wartosci_pt, wartosc_progu):
        wyjscie = []
        for value in wartosci_pt:
            if abs(value) < abs(wartosc_progu): #musi być abs, bo inaczej nie działa tłumienie
                wyjscie.append(0)
            else:
                wyjscie.append(1)
        return wyjscie

    wartosci_ct = PSK_ct(wartosci_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N, wartosc_progu):
        bity = []
        for i in range(0, N, fs):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + fs]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N, wartosc_progu)
    return odczytane

def modulacjaASK(string2):
    def KluczowanieASK(string2, A1, A2, fn, fs, Tb):
        wyjscie1 = []
        wyjscie2 = []
        for n in range(0, N-1):
            t = n / fs
            indeks = int(t / Tb)
            wyjscie1.append(t)

            if string2[indeks] == '0':
                wyjscie2.append(A1 * (math.sin(2 * math.pi * fn * t)))
            else:
                wyjscie2.append(A2 * (math.sin(2 * math.pi * fn * t)))
        return wyjscie1, wyjscie2
    A1 =1
    A2 = 2
    x, y = KluczowanieASK(string2, A1, A2, fn, fs, Tb)
    return x, y

def demodulacjaASK(x, y):
    def ASK_xt(y_ASK, fn, fs):
        wyjscie = []
        A = 1
        for n in range(len(y_ASK)):
            t = n / fs
            wyjscie.append(y[n] * (A * np.sin(2 * np.pi * fn * t)))
        return wyjscie

    wartosci_XT = ASK_xt(y, fn, fs)

    def ASK_pt(wartosci_XT, M, fs):
        dt = 1 / fs
        calka = []
        for i in range(0, len(wartosci_XT), N):
            calka_bit = []
            suma = 0
            for j in range(N):
                if i + j < len(wartosci_XT):
                    suma += wartosci_XT[i + j] * dt
                    calka_bit.append(suma)
            calka.extend(calka_bit)
        return calka

    wartosci_pt = ASK_pt(wartosci_XT, N, fs)

    # def prog_h(x, N, margin=0.05):
    #     wartosc = x[N - 1]  # wartość na końcu pierwzsego bitu
    #     return wartosc - 0.001

    wartosc_progu = 0.01

    def ASK_ct(wartosci_pt, wartosc_progu):
        wyjscie = []
        for value in wartosci_pt:
            if abs(value) >= abs(wartosc_progu):
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = ASK_ct(wartosci_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N, wartosc_progu):
        bity = []
        for i in range(0, N, fs):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + fs]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N, wartosc_progu)
    return odczytane

def modulacjaFSK(string2):
    A1 = 1
    A2 = 2
    def KluczowanieFSK(string2, A1, A2, fn1, fn2, fs, Tb):
        wyjscieFSK1 = []
        wyjscieFSK2 = []

        for n in range(0, N-1):
            t = n / fs
            indeks = int(t / Tb)
            wyjscieFSK1.append(t)
            if string2[indeks] == '0':
                wyjscieFSK2.append(A1 * np.sin(2 * np.pi * fn1 * t))
            else:
                wyjscieFSK2.append(
                    A2 * np.sin(2 * np.pi * fn2 * t))  # Dodanie zer, gdy indeks jest poza zakresem lub bit to '1'
        return wyjscieFSK1, wyjscieFSK2

    x_FSK, y_FSK = KluczowanieFSK(string2, A1, A2, fn1, fn2, fs, Tb)
    return x_FSK, y_FSK

def demodulacjaFSK( x_FSK, y_FSK):
    def FSK_x1_t(y_FSK, fn1, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn1 * t)))
        return wyjscie

    fsk_t_x1 = FSK_x1_t(y_FSK, fn1, fs)

    def FSK_x2_t(y_FSK, fn2, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn2 * t)))
        return wyjscie

    fsk_t_x2 = FSK_x2_t(y_FSK, fn2, fs)

    def FSK_p1_t(fsk_t_x1, N, fs):
        calki = []
        dt = 1 / fs
        for i in range(0, len(fsk_t_x1), N):
            calka_bit = []
            suma = 0
            for j in range(N):
                if i + j < len(fsk_t_x1):
                    suma += fsk_t_x1[i + j] * dt
                    calka_bit.append(suma)
            calki.extend(calka_bit)
        return calki

    fp1_calki = FSK_p1_t(fsk_t_x1, N, fs)

    def FSK_p2_t(fsk_t_x2, N, fs):
        calki = []
        dt = 1 / fs
        for i in range(0, len(fsk_t_x2), N):
            calka_bit = []
            suma = 0
            for j in range(N):
                if i + j < len(fsk_t_x2):
                    suma += fsk_t_x2[i + j] * dt
                    calka_bit.append(suma)
            calki.extend(calka_bit)
        return calki

    fp2_calki = FSK_p2_t(fsk_t_x2, N, fs)

    def FSK_p_t(fp1_calki, fp2_calki):
        wynik = []
        if len(fp1_calki) != len(fp2_calki):
            raise ValueError("Długości sygnałów nie są równe")
        else:
            for i in range(len(fp1_calki)):
                wynik.append(fp1_calki[i] - fp2_calki[i])
        return wynik

    FSK_pt = FSK_p_t(fp1_calki, fp2_calki)
    wartosc_progu = 0.01

    def FSK_ct(FSK_pt, wartosc_progu):
        wyjscie = []
        for value in FSK_pt:
            if abs(value) > abs(wartosc_progu):
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = FSK_ct(FSK_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N, wartosc_progu):
        bity = []
        for i in range(0, N, fs):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + fs]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N, wartosc_progu)
    return odczytane

def modelCyfrowy():
    # dane na wejściu
    print("Dane na wejsciu: ", string2)

    # etap 1
    # koder nadmiarowy
    model1 = HammingKoder(list(map(int, string2)))
    print("Kodowanie Hamminga:", model1)

    # etap 2
    # modulator
    modulator, wartosc2 = modulacjaASK(string2)
    #plt.plot(modulator, wartosc2)
    #plt.show()
    print("Modulacja PSK:", modulator)

    # etap 3
    demodulator = demodulacjaASK(modulator, wartosc2)
    print("Demodulacja PSK:", demodulator)

    # etap 4
    dekoder = HammingDekoder(demodulator)
    print("Dekodowanie Hamminga:", dekoder)

    # wyniki
    #print("Wyniki: ", model1, modulator, wartosc2, demodulator, dekoder)

def szum_bialy(modulator, wartosc2, poziom_szumu):
    # Obliczanie mocy szumu
    moc_sygnalu = np.mean(np.abs(modulator)**2)
    moc_szumu = moc_sygnalu * 10**(-poziom_szumu / 10.0)
    # Generowanie szumu białego o takiej samej długości jak modulator
    szum = np.random.randn(len(modulator)) * np.sqrt(moc_szumu)
    # Dodawanie szumu do modulatora
    modulator_z_szumem = modulator + szum
    return modulator_z_szumem

poziom_szumu_dB = 10

def tlumienie(modulator, wartosc2, Beta):
    wynik = []
    for m, w in zip(modulator, wartosc2):
        tłumienie = cmath.exp(-1 * Beta * w)
        wynik.append(m * tłumienie)
    return wynik

# def oblicz_BER(dane_wejsciowe, odczytane):
#     liczba_przeklamanych_bitow = 0
#
#     # Obliczenie liczby przekłamań bitów
#     for i in range(len(dane_wejsciowe)):
#         if dane_wejsciowe[i] != odczytane[i]:
#             liczba_przeklamanych_bitow += 1
#
#     # Obliczenie BER
#     BER = liczba_przeklamanych_bitow / len(dane_wejsciowe)
#     return BER

def oblicz_BER(dane_wejsciowe, odczytane):
    liczba_przeklamanych_bitow = np.sum(dane_wejsciowe != odczytane)
    # Obliczenie BER
    BER = liczba_przeklamanych_bitow/ len(dane_wejsciowe)
    return BER


def zad2():
    #dla PSK
    model1 = HammingKoder(string2)
    modulator, wartosc2 = modulacjaPSK(string2)
    poszumie = szum_bialy(modulator, wartosc2, poziom_szumu_dB)
    demodulator = demodulacjaPSK(modulator, poszumie)
    dekoder = HammingDekoder(demodulator)
    dane_wejsciowe = list(map(int, string2))
    BER = oblicz_BER(dane_wejsciowe, dekoder)
    print("Blad dla kluczowania PSK: ",BER)
    #dla ASK
    modulator1, wartosc21 = modulacjaASK(string2)
    poszumie1 = szum_bialy(modulator1, wartosc21, poziom_szumu_dB)
    demodulator1 = demodulacjaASK(modulator1, poszumie1)
    dekoder1 = HammingDekoder(demodulator1)
    BER1 = oblicz_BER(dane_wejsciowe, dekoder1)
    print("Blad dla kluczowania ASK: ", BER1)
    #Kluczowanie FSK
    modulator11, wartosc211 = modulacjaFSK(string2)
    poszumie11 = szum_bialy(modulator11, wartosc211, poziom_szumu_dB)
    demodulator11 = demodulacjaFSK(modulator11, poszumie11)
    dekoder11 = HammingDekoder(demodulator1)
    BER11 = oblicz_BER(dane_wejsciowe, demodulator11)
    print("Blad dla kluczowania FSK: ", BER11)

def zad3():
    Beta = 7
    model1 = HammingKoder(list(map(int, string2)))
    modulator, wartosc2 = modulacjaPSK(string2)
    potlumieniu= tlumienie(modulator, wartosc2, Beta)
    demodulator = demodulacjaPSK(modulator, potlumieniu)
    dekoder = HammingDekoder(demodulator)
    dane_wejsciowe = list(map(int, string2))
    BER = oblicz_BER(dane_wejsciowe, demodulator)
    print("Blad dla kluczowania PSK: ", BER)
    #opcja dla ASK
    modulatorA, wartosc2A = modulacjaASK(string2)
    potlumieniuA = tlumienie(modulatorA, wartosc2A, Beta)
    demodulatorA = demodulacjaASK(modulatorA, potlumieniuA)
    dekoderA = HammingDekoder(demodulatorA)
    dane_wejscioweA = list(map(int, string2))
    BERA = oblicz_BER(dane_wejscioweA, demodulatorA)
    print("Blad dla kluczowania PSK: ", BERA)
    #Dla kluczowania FSK
    modulatorF, wartosc2F = modulacjaFSK(string2)
    potlumieniuF = tlumienie(modulatorF, wartosc2F, Beta)
    demodulatorF = demodulacjaFSK(modulatorF, potlumieniuF)
    dekoderF = HammingDekoder(demodulatorF)
    dane_wejscioweF = list(map(int, string2))
    BERF = oblicz_BER(dane_wejscioweF, demodulatorF)
    print("Blad dla kluczowania FSK: ", BERF)

def zad4opcja1():
    #1 + 2
    Beta = 3
    # Wariant 1: Poszumienie -> Tłumienie -> Reszta procesu
    model1 = HammingKoder(list(map(int, string2)))
    modulator, wartosc2 = modulacjaPSK(string2)
    poszumie = szum_bialy(modulator, wartosc2, poziom_szumu_dB)
    modulator_tlumiony = tlumienie(poszumie, wartosc2, Beta)
    demodulator = demodulacjaPSK(modulator_tlumiony, poszumie)
    dekoder = HammingDekoder(demodulator)
    dane_wejscioweF = list(map(int, string2))
    BERF = oblicz_BER(dane_wejscioweF, demodulator)
    print("Blad dla kluczowania FSK: ", BERF)
    # opcja dla ASK
    modulatorA, wartosc2A = modulacjaASK(string2)
    poszumie1 = szum_bialy(modulatorA, wartosc2A, poziom_szumu_dB)
    modulator_tlumiony1 = tlumienie(poszumie1, wartosc2A, Beta)
    demodulatorA = demodulacjaASK(modulatorA, modulator_tlumiony1)
    dekoderA = HammingDekoder(demodulatorA)
    dane_wejscioweA = list(map(int, string2))
    BERA = oblicz_BER(dane_wejscioweA, demodulatorA)
    print("Blad dla kluczowania PSK: ", BERA)
    # Dla kluczowania FSK
    modulatorF, wartosc2F = modulacjaFSK(string2)
    poszumieF = szum_bialy(modulatorF, wartosc2F, poziom_szumu_dB)
    modulator_tlumionyF = tlumienie(poszumieF, wartosc2F, Beta)
    demodulatorF = demodulacjaFSK(modulatorF, modulator_tlumionyF)
    dekoderF = HammingDekoder(demodulatorF)
    dane_wejscioweF = list(map(int, string2))
    BERF = oblicz_BER(dane_wejscioweF, demodulatorF)
    print("Blad dla kluczowania FSK: ", BERF)

def zad4opcja2():
    Beta = 3
    # Wariant 2: Tłumienie -> Poszumienie -> Reszta procesu
    model1 = HammingKoder(list(map(int, string2)))
    modulator, wartosc2 = modulacjaPSK(string2)
    modulator_tlumiony = tlumienie(modulator, wartosc2, Beta)
    poszumie = szum_bialy(modulator_tlumiony, wartosc2, poziom_szumu_dB)
    demodulator = demodulacjaPSK(modulator_tlumiony, poszumie)
    dekoder = HammingDekoder(demodulator)
    dane_wejscioweF = list(map(int, string2))
    BERF = oblicz_BER(dane_wejscioweF, demodulator)
    print("Blad dla kluczowania FSK: ", BERF)
    #kluczowanie ASK
    modulatorA, wartosc2A = modulacjaASK(string2)
    modulator_tlumiony1 = tlumienie(modulatorA, wartosc2A, Beta)
    poszumie1 = szum_bialy(modulator_tlumiony1, wartosc2A, poziom_szumu_dB)
    demodulatorA = demodulacjaASK(modulator_tlumiony1, poszumie1)
    dekoderA = HammingDekoder(demodulatorA)
    dane_wejscioweA = list(map(int, string2))
    BERA = oblicz_BER(dane_wejscioweA, demodulatorA)
    print("Blad dla kluczowania PSK: ", BERA)
    #kluczowanie FSK
    modulatorF, wartosc2F = modulacjaFSK(string2)
    modulator_tlumionyF = tlumienie(modulatorF, wartosc2F, Beta)
    poszumieF = szum_bialy(modulator_tlumionyF, wartosc2F, poziom_szumu_dB)
    demodulatorF = demodulacjaFSK(modulator_tlumionyF, poszumieF)
    dekoderF = HammingDekoder(demodulatorF)
    dane_wejscioweF = list(map(int, string2))
    BERF = oblicz_BER(dane_wejscioweF, demodulatorF)
    print("Blad dla kluczowania PSK: ", BERF)


#modelCyfrowy()
zad2()
zad3()
zad4opcja1()
zad4opcja2()