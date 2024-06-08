# import numpy as np
# import matplotlib.pyplot as plt
# import math
#
#
# #zad 1
# x = [1, 1, 0, 1]
# string1 = 'Do testow'
#
# def zamiana(string1):
#     string3 = ''
#     for i in string1:
#         string3 += bin(ord(i))[2:].zfill(8)
#     return string3
#
# string2 = zamiana(string1)
# Tb = 1
# W = 2
# fn = W * pow(Tb, -1)
# Tc = Tb * len(string2)
# fs = 200
# fi = 180
# f = 1000
# M = int(Tc * fs)
# N = len(string2)*M
# fn1 = (W + 1) / Tb
# fn2 = (W + 2) / Tb
#
# def HammingKoder(x):
#     x1 = np.zeros(7, int)
#     x1[2]=x[0]
#     x1[4]=x[1]
#     x1[5]=x[2]
#     x1[6]=x[3]
#     a = ((x1[2]+x1[4]+x1[6])%2)
#     b = ((x1[2]+x1[5]+x1[6])%2)
#     c = ((x1[4]+x1[5]+x1[6])%2)
#     x1[0]=a
#     x1[1]=b
#     x1[3]=c
#     return x1
#
# def modulacjaASK(x1):
#     string2 = x1
#     def KluczowanieASK(string2, A1, A2, fn, fs, Tb):
#         wyjscie1 = []
#         wyjscie2 = []
#         for n in range(0, N):
#             t = n / fs
#             indeks = int(t / Tb)
#             wyjscie1.append(t)
#
#             if string2[indeks] == '0':
#                 wyjscie2.append(A1 * (math.sin(2 * math.pi * fn * t)))
#             else:
#                 wyjscie2.append(A2 * (math.sin(2 * math.pi * fn * t)))
#         return wyjscie1, wyjscie2
#     A1 =1
#     A2 = 2
#     x, y = KluczowanieASK(string2, A1, A2, fn, fs, Tb)
#
#     #ASK po pomnożeniu przez sunusa
#     def ASK_xt(y_ASK, fn, fs):
#         wyjscie = []
#         A = 1
#         for n in range(len(y_ASK)):
#             t = n / fs
#             wyjscie.append(y[n] * (A * np.sin(2 * np.pi * fn * t)))
#         return wyjscie
#
#     wartosci_XT = ASK_xt(y, fn, fs)
#
#     def ASK_pt(wartosci_XT, M, fs):
#         dt = 1 / fs
#         calka = []
#         for i in range(0, len(wartosci_XT), M):
#             calka_bit = []
#             suma = 0
#             for j in range(M):
#                 if i + j < len(wartosci_XT):
#                     suma += wartosci_XT[i + j] * dt
#                     calka_bit.append(suma)
#             calka.extend(calka_bit)
#         return calka
#
#     wartosci_pt = ASK_pt(wartosci_XT, M, fs)
#
#     def prog_h(x, M, margin=0.05):
#         wartosc = x[M-1] #wartość na końcu pierwzsego bitu
#         return wartosc - 0.001
#
#     wartosc_progu = prog_h(wartosci_pt, M)
#
#     #po progu, czuli c(t)
#     def ASK_ct(wartosci_pt, wartosc_progu):
#         wyjscie = []
#         for value in wartosci_pt:
#             if value >= wartosc_progu:
#                 wartosc1 = 1
#                 wyjscie.append(wartosc1)
#             else:
#                 wartosc = 0
#                 wyjscie.append(wartosc)
#         return wyjscie
#
#     wartosci_ct = ASK_ct(wartosci_pt, wartosc_progu)
#     return wartosci_ct, wartosc_progu
#
# def demodulacja(wartosci_ct, wartosc_progu):
#     def odczytywanie_bitow_ct(wartosci_ct, M, wartosc_progu):
#         bity = []
#         for i in range(0, len(wartosci_ct), M):
#             wartosci1 = 0
#             wartosci = 0
#             for j in wartosci_ct[i:i + M]:
#                 if j == 1:
#                     wartosci1 += 1
#                 elif j == 0:
#                     wartosci += 1
#                 else:
#                     print("blad :(")
#
#             if wartosci1 > wartosci:
#                 bity.append(1)
#             else:
#                 bity.append(0)
#         return bity
#
#     odczytane=odczytywanie_bitow_ct(wartosci_ct, M, wartosc_progu)
#     return odczytane
#
# def HammingDekoder(x1):
#     x2=np.zeros(4, int)
#     x2[0]=x1[2]
#     x2[1]=x1[4]
#     x2[2]=x1[5]
#     x2[3]=x1[6]
#     x1prim = (x1[2]+x1[4]+x1[6])%2
#     x1prim2 = ((x1[2]+x1[5]+x1[6])%2)
#     x1prim4 = ((x1[4]+x1[5]+x1[6])%2)
#     x1daszek = (x1[0] + x1prim)%2
#     x2daszek = ((x1[1] + x1prim2)%2)
#     x4daszek = ((x1[3] + x1prim4)%2)
#     S = ((x1daszek*pow(2,0)) + (x2daszek*pow(2,1)) + (x4daszek*pow(2,2)))
#     return x2, S
#
# def modelCyfrowy():
#     #etap 1
#     #koder nadmiarowy
#     model1 = HammingKoder(string2)
#     print(model1)
#     #print(string2)
#     # reszta = len(string1) %7
#     # print(reszta)
#     #kontrolne = HammingKoder(x) do sprawdzenia, czy koder nie działa tak samo w każdym przypadku
#     #print(model1)
#     #print(kontrolne)
#
#     #etap 2
#     #modulator
#     modulator, wartosc2 = modulacjaASK(model1)
#
#     #etap3
#     demodulator = demodulacja(modulator, wartosc2)
#
#     #etap4
#     #dekoder
#     dekoder = HammingDekoder(demodulator)
#
# modelCyfrowy()

import numpy as np
import matplotlib.pyplot as plt
import math

# zad 1
x = [1, 1, 0, 1]
string1 = 'Do testowania modelu'

def zamiana(string1):
    string3 = ''
    for i in string1:
        string3 += bin(ord(i))[2:].zfill(8)
    return string3

string2 = zamiana(string1)
Tb = 1
W = 2
fn = W * pow(Tb, -1)
Tc = Tb * len(string2)
fs = 200
fi = 180
f = 1000
M = int(Tc * fs)
N = len(string2) * M
fn1 = (W + 1) / Tb
fn2 = (W + 2) / Tb

def HammingKoder(x):
    x1 = np.zeros(7, int)
    x1[2] = x[0]
    x1[4] = x[1]
    x1[5] = x[2]
    x1[6] = x[3]
    a = ((x1[2] + x1[4] + x1[6]) % 2)
    b = ((x1[2] + x1[5] + x1[6]) % 2)
    c = ((x1[4] + x1[5] + x1[6]) % 2)
    x1[0] = a
    x1[1] = b
    x1[3] = c
    return x1

def modulacja(string2):
    def KluczowaniePSK(string2, A1, A2, fn, fs, Tb):
        wyjsciePSK1 = []
        wyjsciePSK2 = []
        for n in range(0, N):
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

    def PSK_xt(y_PSK, fn, fs):
        wyjscie = []
        for n in range(len(y_PSK)):
            t = n / fs
            wyjscie.append(y_PSK[n] * (np.sin(2 * np.pi * fn * t)))
        return wyjscie

    wartosci_XT = PSK_xt(y_PSK, fn, fs)

    def PSK_pt(wartosci_XT, M, fs):
        dt = 1 / fs
        calka = []
        for i in range(0, len(wartosci_XT), M):
            calka_bit = []
            suma = 0
            for j in range(M):
                if i + j < len(wartosci_XT):
                    suma += wartosci_XT[i + j] * dt
                    calka_bit.append(suma)
            calka.extend(calka_bit)
        return calka

    wartosci_pt = PSK_pt(wartosci_XT, M, fs)

    wartosc_progu = 0.01

    def PSK_ct(wartosci_pt, wartosc_progu):
        wyjscie = []
        for value in wartosci_pt:
            if value < wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = PSK_ct(wartosci_pt, wartosc_progu)
    return wartosci_ct, wartosc_progu

def demodulacja(wartosci_ct, wartosc_progu):
    def odczytywanie_bitow_ct(wartosci_ct, M, wartosc_progu):
        bity = []
        for i in range(0, len(wartosci_ct), M):
            wartosci1 = 0
            wartosci = 0
            for j in wartosci_ct[i:i + M]:
                if j == 1:
                    wartosci1 += 1
                elif j == 0:
                    wartosci += 1
                else:
                    print("blad :(")

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane = odczytywanie_bitow_ct(wartosci_ct, M, wartosc_progu)
    return odczytane

def HammingDekoder(x1):
    print("Dane wejściowe do HammingDekoder:", x1)  # Dodane dla debugowania
    x1_len = len(x1)
    if x1_len % 7 != 0:
        print("Błąd: Niepoprawna długość wejścia")
        return None, None  # Obsłuż błąd, zwróć None
    num_bits = x1_len // 7 * 4
    x2 = np.zeros(num_bits, int)
    for i in range(x1_len // 7):
        x2[i * 4] = x1[i * 7 + 2]
        x2[i * 4 + 1] = x1[i * 7 + 4]
        x2[i * 4 + 2] = x1[i * 7 + 5]
        x2[i * 4 + 3] = x1[i * 7 + 6]
    x1prim = sum(x1[2::7]) % 2
    x1prim2 = sum(x1[3::7]) % 2
    x1prim4 = sum(x1[5::7]) % 2
    x1daszek = (x1[0] + x1prim) % 2
    x2daszek = (x1[1] + x1prim2) % 2
    x4daszek = (x1[4] + x1prim4) % 2
    S = ((x1daszek * pow(2, 0)) + (x2daszek * pow(2, 1)) + (x4daszek * pow(2, 2)))
    return x2, S

def modelCyfrowy():
    # etap 1
    # koder nadmiarowy
    model1 = HammingKoder(x)
    print("Kodowanie Hamminga:", model1)

    # etap 2
    # modulator
    modulator, wartosc2 = modulacja(string2)
    print("Modulacja ASK:", modulator)

    # etap 3
    demodulator = demodulacja(modulator, wartosc2)
    print("Demodulacja ASK:", demodulator)

    # etap 4
    # dekoder
    decoded_data = []
    for i in range(0, len(demodulator), 7):  # podziel dane na segmenty po 7 bitów
        segment = demodulator[i:i+7]
        if len(segment) == 7:
            print("Segment do dekodowania:", segment)
            decoded_segment, S = HammingDekoder(segment)
            decoded_data.extend(decoded_segment)

    print("Odkodowane dane:", decoded_data)


modelCyfrowy()