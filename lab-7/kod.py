from ast import Name
from binascii import a2b_qp
import numpy as np
import matplotlib.pyplot as plt
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
Tb = 100
W = 2
fn = W * pow(Tb, -1)
fs = 100
B = 1
Tc = Tb / B
fi = 180
f = 1000
N = int(Tc * fs)
M = len(string2) * N
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
    x1 = np.array(x1, dtype=int)

    if len(x1) < 7:
        raise ValueError("Input array is too small. Expected at least 7 elements.")

    # Obliczanie syndromu błędów
    x1prim = (x1[2] + x1[4] + x1[6]) % 2
    x1prim2 = (x1[2] + x1[5] + x1[6]) % 2
    x1prim4 = (x1[4] + x1[5] + x1[6]) % 2

    x1daszek = (x1[0] + x1prim) % 2
    x2daszek = (x1[1] + x1prim2) % 2
    x4daszek = (x1[3] + x1prim4) % 2

    # Obliczanie pozycji błędu
    S = (x1daszek * 1) + (x2daszek * 2) + (x4daszek * 4)

    # Korekcja błędu, jeśli syndrom wskazuje na błędną pozycję
    # if S != 0:
    #     x1[S - 1] = (x1[S - 1] + 1) % 2

    # Ponowne obliczenie syndromu po korekcji błędu
    x1prim = (x1[0] + x1[2] + x1[4] + x1[6]) % 2
    x1prim2 = (x1[1] + x1[2] + x1[5] + x1[6]) % 2
    x1prim4 = (x1[3] + x1[4] + x1[5] + x1[6]) % 2

    S_po_korekcji = (x1prim * 1) + (x1prim2 * 2) + (x1prim4 * 4)

    # Wydobycie bitów informacji
    x2 = x1[[2, 4, 5, 6]]

    return x2, S, S_po_korekcji


A1 = 0.5
A2 = 1


# def KluczowanieASK(string2, A1, A2, fn, fs, Tb):
#     wyjscie1 = []
#     wyjscie2 = []
#     for n in range(0, N-1):
#         t = n / fs
#         indeks = int(t / Tb)
#         wyjscie1.append(t)

#         if string2[indeks] == '0':
#             wyjscie2.append(A1 * (cmath.sin(2 * cmath.pi * fn * t)))
#         else:
#             wyjscie2.append(A2 * (cmath.sin(2 * cmath.pi * fn * t)))
#     return wyjscie2
def KluczowanieASK(string2, A1, A2, fn, Tb, fs):
    wyjscie = []
    for bit in string2:
        A = A1 if bit == 0 else A2
        for i in range(N):
            t = i / fs
            wyjscie.append(A * cmath.sin(2 * cmath.pi * fn * t))
    return wyjscie


# --------------to działa----------------
model_1 = HammingKoder(string2)
print(model_1)
zA_from_t_ASK = KluczowanieASK(model_1, A1, A2, fn, Tb, fs)


# plt.plot(zA_from_t_ASK, label='ASK')
# plt.title('Wykres ASK dla danych po kodowaniu Hamminga')
# plt.xlabel('Próbki')
# plt.ylabel('Amplituda')
# plt.show()

def demodulacjaASK(y):
    def ASK_xt(y, fn, fs):
        wyjscie = []
        A = 1
        for n in range(len(y)):
            t = n / fs
            wyjscie.append(y[n] * (A * np.sin(2 * np.pi * fn * t)))
        return wyjscie

    # --------------to działa-------------
    wynik = ASK_xt(y, fn, fs)

    # plt.plot(wynik, label = "ASK")
    # plt.show()

    def ASK_pt(wartosci_XT, N, fs):
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

    # ----------------to działa----------------
    wartosci_pt = ASK_pt(wynik, N, fs)
    # plt.plot(wartosci_pt, label = "ASK po całce")
    # plt.show()

    # def prog_h(x, N, margin=0.05):
    #     wartosc = x[N - 1]  # wartość na końcu pierwzsego bitu
    #     return wartosc - 0.001

    wartosc_progu = 20.01

    def ASK_ct(wartosci_pt, wartosc_progu):
        wyjscie = []
        for value in wartosci_pt:
            if value.real >= wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = ASK_ct(wartosci_pt, wartosc_progu)

    # -------------to działa------------
    # plt.plot(wartosci_ct, label = "Wartosci po progu")
    # plt.show()

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)
    return odczytane


# ---------------------------PSK-------------------------

# def kluczowaniePSK(string2, fn, fs, Tb):
#       wyjsciePSK1 = []
#       wyjsciePSK2 = []
#       for n in range(0, N - 1):
#           t = n / fs
#           indeks = int(t / Tb)
#           wyjsciePSK1.append(t)

#           if string2[indeks] == '0':
#               wyjsciePSK2.append(cmath.sin(2 * cmath.pi * fn * t))
#           else:
#               wyjsciePSK2.append(cmath.sin(2 * cmath.pi * fn * t + cmath.pi))
#       return wyjsciePSK2

def kluczowaniePSK(string2, fn, Tb, fs):
    zp = []
    for bit in string2:
        phase = 0 if bit == 0 else cmath.pi
        for i in range(N):
            t = float(i) / fs
            zp.append(cmath.sin(2 * cmath.pi * fn * t + phase))
    return zp


# -----------------------to działa-----------------
y1 = kluczowaniePSK(model_1, fn, fs, Tb)


# plt.plot(y1, label = "Kluczowanie psk")
# plt.show()

def demodulacjaPSK(y_PSK):
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
            if value.real < wartosc_progu:
                wyjscie.append(0)
            else:
                wyjscie.append(1)
        return wyjscie

    wartosci_ct = PSK_ct(wartosci_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)
    return odczytane


# ------------------------------------FSK-----------------------------------

def kluczowanieFSK(string2, Tb, fs, A=1, W=2):
    wyjscie = []

    fn1 = (W + A) / Tb  # częstotliwość dla bitu '0'
    fn2 = (W + (A + 1)) / Tb  # częstotliwość dla bitu '1'

    for bit in string2:
        fn = fn1 if bit == 0 else fn2

        for i in range(N):
            t = float(i) / fs
            wyjscie.append(cmath.sin(2 * cmath.pi * fn * t))

    return wyjscie


y = kluczowanieFSK(model_1, Tb, fs, A=1, W=1)


# --------------to działa----------
# plt.plot(y)
# plt.show()

def demodulacjaFSK(y_FSK):
    def FSK_x1_t(y_FSK, fn1, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn1 * t)))
        return wyjscie

    y = kluczowanieFSK(model_1, Tb, fs, A=1, W=1)
    fsk_t_x1 = FSK_x1_t(y, fn1, fs)

    # ---------------to działa----------------
    # plt.plot(fsk_t_x1, label = "Cpos")
    # plt.show()

    def FSK_x2_t(y_FSK, fn2, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn2 * t)))
        return wyjscie

    fsk_t_x2 = FSK_x2_t(y, fn2, fs)

    # plt.plot(fsk_t_x2, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp1_calki, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp2_calki, label = "mam dosc1")
    # plt.show()

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
            if value.real < wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = FSK_ct(FSK_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)
    return odczytane


# ----------zadanie 1---------------
def modelASK():
    model_1 = HammingKoder(string2)
    print(model_1)
    y = KluczowanieASK(model_1, A1, A2, fn, Tb, fs)
    c = demodulacjaASK(y)
    dekoder = HammingDekoder(c)
    print(dekoder)


def modelPSK():
    model_1 = HammingKoder(string2)
    print(model_1)
    y = kluczowaniePSK(model_1, fn, Tb, fs)
    c = demodulacjaPSK(y)
    print(c)
    dekoder = HammingDekoder(c)
    print(dekoder)


def modelFSK():
    model_1 = HammingKoder(string2)
    print(model_1)
    y = kluczowanieFSK(model_1, Tb, fs, A=1, W=1)
    c = demodulacjaFSK(y)
    print(c)
    dekoder = HammingDekoder(c)
    print(dekoder)


# ------------zadanie 2--------------------

def dodaj_szum_bialy(sygnał, amplituda_szumu):
    szum = np.random.normal(0, amplituda_szumu, len(sygnał))  # Generowanie szumu gaussowskiego
    sygnał_z_szumem = sygnał + szum  # połączenie sygnału z szumem
    return sygnał_z_szumem


def oblicz_BER(dane_oryginalne, dane_odebrane):
    if len(dane_oryginalne) != len(dane_odebrane):
        raise ValueError("Długości danych oryginalnych i otrzymanych muszą być równe")

    ilosc_bledow = sum(1 for bit_oryg, bit_odeb in zip(dane_oryginalne, dane_odebrane) if bit_oryg != bit_odeb)
    BER = ilosc_bledow / len(dane_oryginalne)
    return BER


# def tlumienieFunkcja(modulator, wartosc2, Beta):
#     wynik = []
#     for m, w in zip(modulator, wartosc2):
#         tłumienie = cmath.exp(-1 * Beta * w)
#         wynik.append(m * tłumienie)
#     return wynik

def tlumienieFunkcja(modulator, wartosc2, Beta):
    wartosc2 = np.array(wartosc2)
    modulator = np.array(modulator)
    tlumienie = np.exp(-Beta * wartosc2)
    wynik = modulator * tlumienie
    return wynik.tolist()

def zad2ASK():
    amplituda_szumu = 2000
    model_1 = HammingKoder(string2)
    print(model_1)

    y = KluczowanieASK(model_1, A1, A2, fn, Tb, fs)

    def ASK_xt(y, fn, fs):
        wyjscie = []
        A = 1
        for n in range(len(y)):
            t = n / fs
            wyjscie.append(y[n] * (A * np.sin(2 * np.pi * fn * t)))
        return wyjscie

    # --------------to działa-------------
    wynik = ASK_xt(y, fn, fs)

    # plt.plot(wynik, label = "ASK")
    # plt.show()

    def ASK_pt(wartosci_XT, N, fs):
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

    # ----------------to działa----------------
    wartosci_pt = ASK_pt(wynik, N, fs)
    # plt.plot(wartosci_pt, label = "ASK po całce")
    # plt.show()

    # def prog_h(x, N, margin=0.05):
    #     wartosc = x[N - 1]  # wartość na końcu pierwzsego bitu
    #     return wartosc - 0.001

    wartosc_progu = 20.01

    def ASK_ct(wartosci_pt, wartosc_progu):
        wyjscie = []
        for value in wartosci_pt:
            if value.real >= wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = ASK_ct(wartosci_pt, wartosc_progu)

    # -------------to działa------------
    # plt.plot(wartosci_ct, label = "Wartosci po progu")
    # plt.show()

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_szum = dodaj_szum_bialy(y, amplituda_szumu)
    wynik_szum = ASK_xt(y_szum, fn, fs)
    wartosc_pt_szum = ASK_pt(wynik_szum, N, fs)
    wartosci_ct_szum = ASK_ct(wartosc_pt_szum, wartosc_progu)
    odczytane_szum = odczytywanie_bitow_ct(wartosci_ct_szum, N)
    print("WArtości odczytane bez szumu: ", odczytane)
    print("Wartości z szumem z ASK: ", odczytane_szum)
    szum, _, _ = HammingDekoder(odczytane_szum)
    print("Dekodawane dane z szumem: ", szum)
    BER = oblicz_BER(odczytane, odczytane_szum)
    print(BER)
    return BER


# -----------PSK---------------

def zad2PSK():
    amplituda_szumu = 500
    model_1 = HammingKoder(string2)
    print(model_1)
    y = kluczowaniePSK(model_1, fn, Tb, fs)

    def PSK_xt(y_PSK, fn, fs):
        wyjscie = []
        for n in range(len(y_PSK)):
            t = n / fs
            wyjscie.append(y_PSK[n] * (np.sin(2 * np.pi * fn * t)))
        return wyjscie

    wartosci_XT = PSK_xt(y, fn, fs)

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
            if value.real < wartosc_progu:
                wyjscie.append(0)
            else:
                wyjscie.append(1)
        return wyjscie

    wartosci_ct = PSK_ct(wartosci_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_szum = dodaj_szum_bialy(y, amplituda_szumu)
    wartosci_XT_szum = PSK_xt(y_szum, fn, fs)
    wartosci_pt_szum = PSK_pt(wartosci_XT_szum, N, fs)
    wartosci_ct_szum = PSK_ct(wartosci_pt_szum, wartosc_progu)
    odczytane_szum = odczytywanie_bitow_ct(wartosci_ct_szum, N)
    print("WArtości odczytane bez szumu: ", odczytane)
    print("Wartości z szumem z PSK: ", odczytane_szum)
    szum, _, _ = HammingDekoder(odczytane_szum)
    print("Dekodawane dane z szumem: ", szum)
    BER = oblicz_BER(odczytane, odczytane_szum)
    print(BER)
    return BER


# -------------------FSK----------------------

def zad2FSK():
    amplituda_szumu = 500

    def FSK_x1_t(y_FSK, fn1, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn1 * t)))
        return wyjscie

    y = kluczowanieFSK(model_1, Tb, fs, A=1, W=1)
    fsk_t_x1 = FSK_x1_t(y, fn1, fs)

    # ---------------to działa----------------
    # plt.plot(fsk_t_x1, label = "Cpos")
    # plt.show()

    def FSK_x2_t(y_FSK, fn2, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn2 * t)))
        return wyjscie

    fsk_t_x2 = FSK_x2_t(y, fn2, fs)

    # plt.plot(fsk_t_x2, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp1_calki, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp2_calki, label = "mam dosc1")
    # plt.show()

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
            if value.real < wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = FSK_ct(FSK_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_szum = dodaj_szum_bialy(y, amplituda_szumu)
    zf_x1_t = FSK_x1_t(y_szum, fn1, fs)
    zf_x2_t = FSK_x2_t(y_szum, fn2, fs)
    zf_p1_t = FSK_p1_t(zf_x1_t, N, fs)
    zf_p2_t = FSK_p2_t(zf_x2_t, N, fs)
    zf_p_t = FSK_p_t(zf_p1_t, zf_p2_t)
    prog = 0.01
    zf_c_t = FSK_ct(zf_p_t, prog)
    odczytane_bity_szum = odczytywanie_bitow_ct(zf_c_t, N)
    print("Odczytane bity z szumem: ", odczytane_bity_szum)
    print("Odczytane bity bez szumu: ", odczytane)
    xFSK, _, _ = HammingDekoder(odczytane)
    print("Dekodowane dane bez szumu: ", odczytane)
    zdekodowane_dane_szum = HammingDekoder(odczytane_bity_szum)
    print("Dekodowane dane z szumem: ", zdekodowane_dane_szum)
    BER_FSK = oblicz_BER(odczytane, odczytane_bity_szum)
    print("Bit Error Rate (BER):", BER_FSK)
    return BER_FSK


def zad3ASK():
    Beta = 9
    amplituda_szumu = 10000
    model_1 = HammingKoder(string2)
    print(model_1)

    y = KluczowanieASK(model_1, A1, A2, fn, Tb, fs)

    def ASK_xt(y_ASK, fn, fs):
        wyjscie = []
        A = 1
        for n in range(len(y_ASK)):
            t = n / fs
            wyjscie.append(y[n] * (A * np.sin(2 * np.pi * fn * t)))
        return wyjscie

    # --------------to działa-------------
    wynik = ASK_xt(y, fn, fs)

    # plt.plot(wynik, label = "ASK")
    # plt.show()

    def ASK_pt(wartosci_XT, N, fs):
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

    # ----------------to działa----------------
    wartosci_pt = ASK_pt(wynik, N, fs)
    # plt.plot(wartosci_pt, label = "ASK po całce")
    # plt.show()

    # def prog_h(x, N, margin=0.05):
    #     wartosc = x[N - 1]  # wartość na końcu pierwzsego bitu
    #     return wartosc - 0.001

    wartosc_progu = 20.01

    def ASK_ct(wartosci_pt, wartosc_progu):
        wyjscie = []
        for value in wartosci_pt:
            if value.real >= wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = ASK_ct(wartosci_pt, wartosc_progu)

    # -------------to działa------------
    # plt.plot(wartosci_ct, label = "Wartosci po progu")
    # plt.show()

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_tlumienie = tlumienieFunkcja(y, y, Beta)
    wynik_tlumienie = ASK_xt(y_tlumienie, fn, fs)
    wartosc_pt_tlumienie = ASK_pt(wynik_tlumienie, N, fs)
    wartosci_ct_tlumienie = ASK_ct(wartosc_pt_tlumienie, wartosc_progu)
    odczytane_tlumienie = odczytywanie_bitow_ct(wartosci_ct_tlumienie, N)
    print("WArtości odczytane bez tlumienie: ", odczytane)
    print("Wartości z tlumienie z ASK: ", odczytane_tlumienie)
    tlumienie, _, _ = HammingDekoder(odczytane_tlumienie)
    print("Dekodawane dane z tlumienie: ", tlumienie)
    BER = oblicz_BER(odczytane, odczytane_tlumienie)
    print("Wartosc BER dla ASK z tlumieniem: ", BER)
    return BER


def zad3PSK():
    Beta = 7
    amplituda_szumu = 500
    model_1 = HammingKoder(string2)
    print(model_1)
    y = kluczowaniePSK(model_1, fn, Tb, fs)

    def PSK_xt(y_PSK, fn, fs):
        wyjscie = []
        for n in range(len(y_PSK)):
            t = n / fs
            wyjscie.append(y_PSK[n] * (np.sin(2 * np.pi * fn * t)))
        return wyjscie

    wartosci_XT = PSK_xt(y, fn, fs)

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
            if value.real < wartosc_progu:
                wyjscie.append(0)
            else:
                wyjscie.append(1)
        return wyjscie

    wartosci_ct = PSK_ct(wartosci_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_tlumienie = tlumienieFunkcja(y, y, Beta)
    wartosci_XT_tlumienie = PSK_xt(y_tlumienie, fn, fs)
    wartosci_pt_tlumienie = PSK_pt(wartosci_XT_tlumienie, N, fs)
    wartosci_ct_tlumienie = PSK_ct(wartosci_pt_tlumienie, wartosc_progu)
    odczytane_tlumienie = odczytywanie_bitow_ct(wartosci_ct_tlumienie, N)
    print("WArtości odczytane bez szumu: ", odczytane)
    print("Wartości z szumem z PSK: ", odczytane_tlumienie)
    tlumienie, _, _ = HammingDekoder(odczytane_tlumienie)
    print("Dekodawane dane z szumem: ", tlumienie)
    BER = oblicz_BER(odczytane, odczytane_tlumienie)
    print(BER)
    return BER


def zad3FSK():
    Beta = 7
    amplituda_szumu = 500

    def FSK_x1_t(y_FSK, fn1, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn1 * t)))
        return wyjscie

    y = kluczowanieFSK(model_1, Tb, fs, A=1, W=1)
    fsk_t_x1 = FSK_x1_t(y, fn1, fs)

    # ---------------to działa----------------
    # plt.plot(fsk_t_x1, label = "Cpos")
    # plt.show()

    def FSK_x2_t(y_FSK, fn2, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn2 * t)))
        return wyjscie

    fsk_t_x2 = FSK_x2_t(y, fn2, fs)

    # plt.plot(fsk_t_x2, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp1_calki, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp2_calki, label = "mam dosc1")
    # plt.show()

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
            if value.real < wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = FSK_ct(FSK_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_tlumienie = tlumienieFunkcja(y, y, Beta)
    zf_x1_t = FSK_x1_t(y_tlumienie, fn1, fs)
    zf_x2_t = FSK_x2_t(y_tlumienie, fn2, fs)
    zf_p1_t = FSK_p1_t(zf_x1_t, N, fs)
    zf_p2_t = FSK_p2_t(zf_x2_t, N, fs)
    zf_p_t = FSK_p_t(zf_p1_t, zf_p2_t)
    prog = 0.01
    zf_c_t = FSK_ct(zf_p_t, prog)
    odczytane_bity_tlumienie = odczytywanie_bitow_ct(zf_c_t, N)
    print("Odczytane bity z szumem: ", odczytane_bity_tlumienie)
    print("Odczytane bity bez szumu: ", odczytane)
    xFSK, _, _ = HammingDekoder(odczytane)
    print("Dekodowane dane bez szumu: ", odczytane)
    zdekodowane_dane_tlumienie = HammingDekoder(odczytane_bity_tlumienie)
    print("Dekodowane dane z szumem: ", zdekodowane_dane_tlumienie)
    BER_FSK = oblicz_BER(odczytane, odczytane_bity_tlumienie)
    print(BER_FSK)
    return BER_FSK


def zad4PSKwersja1():
    # wersja1
    Beta = 7
    amplituda_szumu = 500
    model_1 = HammingKoder(string2)
    print(model_1)
    y = kluczowaniePSK(model_1, fn, Tb, fs)

    def PSK_xt(y_PSK, fn, fs):
        wyjscie = []
        for n in range(len(y_PSK)):
            t = n / fs
            wyjscie.append(y_PSK[n] * (np.sin(2 * np.pi * fn * t)))
        return wyjscie

    wartosci_XT = PSK_xt(y, fn, fs)

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
            if value.real < wartosc_progu:
                wyjscie.append(0)
            else:
                wyjscie.append(1)
        return wyjscie

    wartosci_ct = PSK_ct(wartosci_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_tlumienie = tlumienieFunkcja(y, y, Beta)
    wartosci_XT_tlumienie = PSK_xt(y_tlumienie, fn, fs)
    wartosci_pt_tlumienie = PSK_pt(wartosci_XT_tlumienie, N, fs)
    wartosci_ct_tlumienie = PSK_ct(wartosci_pt_tlumienie, wartosc_progu)

    y_szum = dodaj_szum_bialy(y, amplituda_szumu)
    wartosci_XT_szum = PSK_xt(y_tlumienie, fn, fs)
    wartosci_pt_szum = PSK_pt(wartosci_XT_szum, N, fs)
    wartosci_ct_szum = PSK_ct(wartosci_pt_szum, wartosc_progu)
    odczytane_szum = odczytywanie_bitow_ct(wartosci_ct_szum, N)
    szum, _, _ = HammingDekoder(odczytane_szum)
    print("WArtości odczytane z szumem i tłumieniem: ", odczytane_szum)
    tlumienie, _, _ = HammingDekoder(odczytane_szum)
    print("Dekodawane dane z szumem: ", tlumienie)

    BER = oblicz_BER(odczytane, odczytane_szum)
    print("BER PSK z szumem i tlumieniem: ", BER)
    return BER


def zad4PSKwersja2():
    # wersja1
    Beta = 7
    amplituda_szumu = 500
    model_1 = HammingKoder(string2)
    print(model_1)
    y = kluczowaniePSK(model_1, fn, Tb, fs)

    def PSK_xt(y_PSK, fn, fs):
        wyjscie = []
        for n in range(len(y_PSK)):
            t = n / fs
            wyjscie.append(y_PSK[n] * (np.sin(2 * np.pi * fn * t)))
        return wyjscie

    wartosci_XT = PSK_xt(y, fn, fs)

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
            if value.real < wartosc_progu:
                wyjscie.append(0)
            else:
                wyjscie.append(1)
        return wyjscie

    wartosci_ct = PSK_ct(wartosci_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_tlumienie = tlumienieFunkcja(y, y, Beta)
    wartosci_XT_tlumienie = PSK_xt(y_tlumienie, fn, fs)
    wartosci_pt_tlumienie = PSK_pt(wartosci_XT_tlumienie, N, fs)
    wartosci_XT_szum_tlumienie = dodaj_szum_bialy(y_tlumienie, amplituda_szumu)

    wartosci_pt_szum_tlumienie = PSK_pt(wartosci_XT_szum_tlumienie, N, fs)
    wartosci_ct_szum_tlumienie = PSK_ct(wartosci_pt_szum_tlumienie, wartosc_progu)
    odczytane_szum_tlumienie = odczytywanie_bitow_ct(wartosci_ct_szum_tlumienie, N)
    szum_tlumienie, _, _ = HammingDekoder(odczytane_szum_tlumienie)
    print("WArtości odczytane z szumem i tłumieniem: ", odczytane_szum_tlumienie)
    tlumienie, _, _ = HammingDekoder(odczytane_szum_tlumienie)
    print("Dekodawane dane z szumem: ", tlumienie)

    BER = oblicz_BER(odczytane, odczytane_szum_tlumienie)
    print("BER PSK z tlumieniem i szumem: ", BER)
    return BER


def zad4FSKwersja1():
    Beta = 7
    amplituda_szumu = 500

    def FSK_x1_t(y_FSK, fn1, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn1 * t)))
        return wyjscie

    y = kluczowanieFSK(model_1, Tb, fs, A=1, W=1)
    fsk_t_x1 = FSK_x1_t(y, fn1, fs)

    # ---------------to działa----------------
    # plt.plot(fsk_t_x1, label = "Cpos")
    # plt.show()

    def FSK_x2_t(y_FSK, fn2, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn2 * t)))
        return wyjscie

    fsk_t_x2 = FSK_x2_t(y, fn2, fs)

    # plt.plot(fsk_t_x2, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp1_calki, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp2_calki, label = "mam dosc1")
    # plt.show()

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
            if value.real < wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = FSK_ct(FSK_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_szum = dodaj_szum_bialy(y, amplituda_szumu)
    zf_x1_t_szum = FSK_x1_t(y_szum, fn1, fs)
    zf_x2_t_szum = FSK_x2_t(y_szum, fn2, fs)
    zf_p1_t_szum = FSK_p1_t(zf_x1_t_szum, N, fs)
    zf_p2_t_szum = FSK_p2_t(zf_x2_t_szum, N, fs)
    zf_p_t_szum = FSK_p_t(zf_p1_t_szum, zf_p2_t_szum)
    zf_p_t_tlumienie_szum = dodaj_szum_bialy(zf_p_t_szum, amplituda_szumu)
    prog = 0.01
    zf_c_t_tlumienie_szum = FSK_ct(zf_p_t_tlumienie_szum, prog)
    odczytane_bity_tlumienie_szum = odczytywanie_bitow_ct(zf_c_t_tlumienie_szum, N)
    print("Odczytane bity z szumem i tlumieniem: ", odczytane_bity_tlumienie_szum)
    print("Odczytane bity bez szumu: ", odczytane)
    xFSK, _, _ = HammingDekoder(odczytane_bity_tlumienie_szum)
    print("Dekodowane dane z szumem szumem i tlumieniem: ", xFSK)
    BER_FSK = oblicz_BER(odczytane, odczytane_bity_tlumienie_szum)
    print("BER FSK z szumem i tlumieniem: ", BER_FSK)
    return BER_FSK


def zad4FSKwersja2():
    Beta = 7
    amplituda_szumu = 500

    def FSK_x1_t(y_FSK, fn1, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn1 * t)))
        return wyjscie

    y = kluczowanieFSK(model_1, Tb, fs, A=1, W=1)
    fsk_t_x1 = FSK_x1_t(y, fn1, fs)

    # ---------------to działa----------------
    # plt.plot(fsk_t_x1, label = "Cpos")
    # plt.show()

    def FSK_x2_t(y_FSK, fn2, fs):
        wyjscie = []
        for n in range(len(y_FSK)):
            t = n / fs
            wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn2 * t)))
        return wyjscie

    fsk_t_x2 = FSK_x2_t(y, fn2, fs)

    # plt.plot(fsk_t_x2, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp1_calki, label = "mam dosc")
    # plt.show()

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

    # plt.plot(fp2_calki, label = "mam dosc1")
    # plt.show()

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
            if value.real < wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = FSK_ct(FSK_pt, wartosc_progu)

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 < wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_tlumienie = tlumienieFunkcja(y, y, Beta)
    zf_x1_t_tlumienie = FSK_x1_t(y_tlumienie, fn1, fs)
    zf_x2_t_tlumienie = FSK_x2_t(y_tlumienie, fn2, fs)
    zf_p1_t_tlumienie = FSK_p1_t(zf_x1_t_tlumienie, N, fs)
    zf_p2_t_tlumienie = FSK_p2_t(zf_x2_t_tlumienie, N, fs)
    zf_p_t_tlumienie = FSK_p_t(zf_p1_t_tlumienie, zf_p2_t_tlumienie)
    zf_p_t_szum_tlumienie = dodaj_szum_bialy(zf_p_t_tlumienie, amplituda_szumu)
    prog = 0.01
    zf_c_t_szum_tlumienie = FSK_ct(zf_p_t_szum_tlumienie, prog)
    odczytane_bity_szum_tlumienie = odczytywanie_bitow_ct(zf_c_t_szum_tlumienie, N)
    print("Odczytane bity z tlumieniem i szumem: ", odczytane_bity_szum_tlumienie)
    print("Odczytane bity bez szumu: ", odczytane)
    xFSK, _, _ = HammingDekoder(odczytane_bity_szum_tlumienie)
    print("Dekodowane dane z szumem szumem i tlumieniem: ", xFSK)
    BER_FSK = oblicz_BER(odczytane, odczytane_bity_szum_tlumienie)
    print("BER FSK z tlumieniem i szumem: ", BER_FSK)
    return BER_FSK


def zad4ASKwersja1():
    Beta = 7
    amplituda_szumu = 1000
    model_1 = HammingKoder(string2)
    print(model_1)

    y = KluczowanieASK(model_1, A1, A2, fn, Tb, fs)

    def ASK_xt(y_ASK, fn, fs):
        wyjscie = []
        A = 1
        for n in range(len(y_ASK)):
            t = n / fs
            wyjscie.append(y[n] * (A * np.sin(2 * np.pi * fn * t)))
        return wyjscie

    # --------------to działa-------------
    wynik = ASK_xt(y, fn, fs)

    # plt.plot(wynik, label = "ASK")
    # plt.show()

    def ASK_pt(wartosci_XT, N, fs):
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

    # ----------------to działa----------------
    wartosci_pt = ASK_pt(wynik, N, fs)
    # plt.plot(wartosci_pt, label = "ASK po całce")
    # plt.show()

    # def prog_h(x, N, margin=0.05):
    #     wartosc = x[N - 1]  # wartość na końcu pierwzsego bitu
    #     return wartosc - 0.001

    wartosc_progu = 20.01

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

    # -------------to działa------------
    # plt.plot(wartosci_ct, label = "Wartosci po progu")
    # plt.show()

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_szum = dodaj_szum_bialy(y, amplituda_szumu)
    wynik_szum = ASK_xt(y_szum, fn, fs)
    wartosc_pt_szum = ASK_pt(wynik_szum, N, fs)
    wartosci_pt_tlumienie_szum = tlumienieFunkcja(wartosc_pt_szum, wartosc_pt_szum, Beta)
    prog = 20.01
    wartosci_ct_tlumienie_szum = ASK_ct(wartosci_pt_tlumienie_szum, prog)
    odczytane_szum_tlumienie = odczytywanie_bitow_ct(wartosci_ct_tlumienie_szum, N)
    print("WArtości odczytane bez szumu: ", odczytane)
    print("Wartości z szumem z szumem i tłumieniem", odczytane_szum_tlumienie)
    tlumienie, _, _ = HammingDekoder(odczytane_szum_tlumienie)
    print("Dekodawane dane z szumem i tłumieniem: ", tlumienie)
    BER = oblicz_BER(odczytane, odczytane_szum_tlumienie)
    print("BER ASK z szumem i tlumieniem: ", BER)
    return BER


def zad4ASKwersja2():
    Beta = 7
    amplituda_szumu = 10000
    model_1 = HammingKoder(string2)
    print(model_1)

    y = KluczowanieASK(model_1, A1, A2, fn, Tb, fs)

    def ASK_xt(y_ASK, fn, fs):
        wyjscie = []
        A = 1
        for n in range(len(y_ASK)):
            t = n / fs
            wyjscie.append(y[n] * (A * np.sin(2 * np.pi * fn * t)))
        return wyjscie

    # --------------to działa-------------
    wynik = ASK_xt(y, fn, fs)

    # plt.plot(wynik, label = "ASK")
    # plt.show()

    def ASK_pt(wartosci_XT, N, fs):
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

    # ----------------to działa----------------
    wartosci_pt = ASK_pt(wynik, N, fs)
    # plt.plot(wartosci_pt, label = "ASK po całce")
    # plt.show()

    # def prog_h(x, N, margin=0.05):
    #     wartosc = x[N - 1]  # wartość na końcu pierwzsego bitu
    #     return wartosc - 0.001

    wartosc_progu = 20.01

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

    # -------------to działa------------
    # plt.plot(wartosci_ct, label = "Wartosci po progu")
    # plt.show()

    def odczytywanie_bitow_ct(wartosci_ct, N):
        bity = []
        for i in range(0, len(wartosci_ct), N):
            wartosci1 = 0
            wartosci = 0

            for j in wartosci_ct[i:i + N]:
                if j == 1:
                    wartosci1 += 1
                else:
                    wartosci += 1

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, N)

    y_tlumienie = tlumienieFunkcja(y, y, Beta)
    wynik_tlumienie = ASK_xt(y_tlumienie, fn, fs)
    wartosc_pt_tlumienie = ASK_pt(wynik_tlumienie, N, fs)
    wartosci_pt_tlumienie_szum = dodaj_szum_bialy(wartosc_pt_tlumienie, amplituda_szumu)
    wartosci_ct_szum_tlumienie = ASK_ct(wartosci_pt_tlumienie_szum, wartosc_progu)
    odczytane_szum = odczytywanie_bitow_ct(wartosci_ct_szum_tlumienie, N)
    print("WArtości odczytane bez szumu: ", odczytane)
    print("Wartości z szumem z szumem i tłumieniem", odczytane_szum)
    tlumienie, _, _ = HammingDekoder(odczytane_szum)
    print("Dekodawane dane z szumem: ", tlumienie)
    BER = oblicz_BER(odczytane, odczytane_szum)
    print("BER ASK z tlumieniem i szumem: ", BER)
    return BER


# modelASK()
# modelPSK()
# modelFSK()
zad2ASK()
zad2PSK()
zad2FSK()
zad3ASK()
zad3PSK()
zad3FSK()
zad4PSKwersja1()
zad4PSKwersja2()
zad4FSKwersja1()
zad4FSKwersja2()
zad4ASKwersja1()
zad4ASKwersja2()