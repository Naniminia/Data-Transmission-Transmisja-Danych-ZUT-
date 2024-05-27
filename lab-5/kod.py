import matplotlib.pyplot as plt
import math
import numpy as np

string1 = 'ABC'

def zamiana(string1):
    string3 = ''
    for i in string1:
        string3 += bin(ord(i))[2:]
    return string3

print("Wartość: ", zamiana(string1))

string2 = zamiana(string1)
Tb = 1
W = 2
fn = W * pow(Tb, -1)
Tc = Tb * len(string2)
fs = 200
fi = 180
f = 1000
N = int(Tc * fs)
fn1 = (W + 1) / Tb
fn2 = (W + 2) / Tb

def sinus(fn, N):
    A = 1
    wynik = []
    x = []
    for n in range(N):
        t = n / fs
        x.append(t)
        wynik.append(A * math.sin(2 * math.pi * fn * t))
    return x, wynik

def kluczowanieASK(string2, fs, fn, Tb):
    A1 = 0
    A2 = 1
    wyjscie1 = []
    wyjscie2 = []

    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t / Tb)
        if string2[indeks] == '0':
            wyjscie2.append(A1 * (math.sin(2 * math.pi * fn * t)))
        else:
            wyjscie2.append(A2 * (math.sin(2 * math.pi * fn * t)))
    return wyjscie1, wyjscie2

def KluczowaniePSK(string2, fs, fn, Tb):
    wyjscie1 = []
    wyjscie2 = []

    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t / Tb)

        if string2[indeks] == '0':
            wyjscie2.append(math.sin(2 * math.pi * fn * t))
        else:
            wyjscie2.append(math.sin(2 * math.pi * fn * t + math.pi))
    return wyjscie1, wyjscie2

def KluczowanieFSK(string2, fs, fn1, Tb):
    wyjscie1 = []
    wyjscie2 = []

    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t / Tb)
        if indeks < len(string2) and string2[indeks] == '0':
            wyjscie2.append(math.sin(2 * math.pi * fn1 * t))
        else:
            wyjscie2.append(0)  # Dodanie zer, gdy indeks jest poza zakresem lub bit to '1'
    return wyjscie1, wyjscie2

def KluczowanieFSK1(string2, fs, fn2, Tb):
    wyjscie1 = []
    wyjscie2 = []

    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t / Tb)
        if indeks < len(string2) and string2[indeks] == '1':
            wyjscie2.append(math.sin(2 * math.pi * fn2 * t))
        else:
            wyjscie2.append(0)  # Dodanie zer, gdy indeks jest poza zakresem lub bit to '0'
    return wyjscie1, wyjscie2

# Definicja funkcji całkującej
def calkowanie(x, y, Tb):
    wynik = []
    suma = 0
    for i in range(len(x)):
        suma += y[i]
        wynik.append(suma * Tb)
    return x, wynik

def porownaj_z_h(x_calka, y_calka, h):
    x_wynik = []
    y_wynik = []
    for i in range(len(x_calka)):
        if y_calka[i] < h:
            x_wynik.append(x_calka[i])
            y_wynik.append(y_calka[i])
    return x_wynik, y_wynik

#klcuzowanie ASK wykresyw wszystkie:
x, y = kluczowanieASK(string2, fs, fn, Tb)
plt.plot(x, y)
plt.show()
plt.savefig('ask_z.png')

x1, y1 = sinus(fn, N)
plt.plot(x1, y1, 'm')
plt.show()
plt.savefig('ask_x.png')

# Tworzenie listy z wartościami bitów (0 lub 1) z ciągu string2
bit_values = [int(char) for char in string2]

# Znajdowanie indeksów zmiany bitów
bit_changes = [i for i in range(1, len(bit_values)) if bit_values[i] != bit_values[i - 1]]

# Rysowanie pionowych linii w miejscach zmiany bitów
for bit_change in bit_changes:
    plt.axvline(x=x1[bit_change], color='gray', linestyle='--')

x_calka, y_calka = calkowanie(x, y, Tb)
h = 0.5
xh, yh = porownaj_z_h(x_calka, y_calka, h)
plt.plot(xh, yh)
plt.show()
plt.savefig("ask_c")

# Wykres całkowania
plt.plot(x_calka, y_calka)
plt.grid(True)
plt.show()
plt.savefig("ask_p")


print("x:", x)
print("y:", y)

# Funkcja wybierająca wartości większe od zera
def wybierz_wieksze_od_zera(x, y):
    wynik = [max(val, 0) for val in y]
    return x, wynik

def wybierz_mniejsze_od_zera(x, y):
    wynik = [min(val, 0) for val in y]
    return x, wynik

#wykresy do KluczowaniaPSK
xp, yp = KluczowaniePSK(string2, fs, fn, Tb)
plt.plot(xp, yp)
plt.show()
plt.savefig('psk_z.png')

xp1, yp1 = sinus(fn, N)
plt.plot(xp1, yp1, 'm')
plt.show()
plt.savefig('psk_x.png')

xp_calka, yp_calka = calkowanie(xp, yp, Tb)
plt.plot(xp, yp)
plt.show()
plt.savefig("psk_p.png")

xpc, ypc = wybierz_mniejsze_od_zera(xp_calka, yp_calka)
plt.plot(xpc, ypc)
plt.show()
plt.savefig("psk_c.png")

#wykresy do kluczowaniaFSK
xf, yf = KluczowanieFSK(string2, fs, fn1, Tb)
plt.plot(xf, yf)
plt.show()
plt.savefig('fsk_z.png')

xf1, yf1 = sinus(fn, N)
plt.plot(xf1, yf1, 'm')
plt.show()
plt.savefig('fsk_x.png')

xf_calka, yf_calka = calkowanie(xf, yf, Tb)
plt.plot(xp, yp)
plt.show()
plt.savefig("fsk_p1.png")

#wykresy do kluczowaniaFSK1
xf_1, yf_1 = KluczowanieFSK1(string2, fs, fn1, Tb)
plt.plot(xf_1, yf_1)
plt.show()

xf11, yf11 = sinus(fn, N)
plt.plot(xf11, yf11, 'm')
plt.show()
plt.savefig('fsk_x1.png')

xf1_calka, yf1_calka = calkowanie(xf_1, yf_1, Tb)
plt.plot(xp, yp)
plt.show()
plt.savefig("fsk_p2.png")

yf_calka_diff = np.array(yf_calka) - np.array(yf1_calka)

xf1c, yf1c = wybierz_wieksze_od_zera(xf1_calka, yf1_calka)
plt.plot(xf_calka, yf_calka_diff)
plt.show()
plt.savefig("fsk_p.png")

xfc, yfc = wybierz_wieksze_od_zera(xf_calka, yf_calka_diff)
plt.plot(xfc, yfc)
plt.show()
plt.savefig("fsk_c.png")


#zadanie 3
def sygnal_na_bity(x_calka, y_calka, h):
    bity = []
    for i in range(len(y_calka)):
        if y_calka[i] < h:
            bity.append(0)
        else:
            bity.append(1)
    return bity

# Wybór odpowiednich wartości progowych h
h_ask = 0.5
h_psk = -0.5  # Dla PSK wybieramy mniejsze od zera wartości, stąd -0.5
h_fsk = 0.5

# Zamiana sygnału c(t) na ciąg bitów dla ASK
bity_ask = sygnal_na_bity(x_calka, y_calka, h_ask)
print("Bity ASK:", bity_ask)

# Zamiana sygnału c(t) na ciąg bitów dla PSK
bity_psk = sygnal_na_bity(xpc, ypc, h_psk)
print("Bity PSK:", bity_psk)

# Zamiana sygnału c(t) na ciąg bitów dla FSK
bity_fsk = sygnal_na_bity(xf_calka, yf_calka_diff, h_fsk)
print("Bity FSK:", bity_fsk)

x_calka, y_calka = calkowanie(x, y, Tb)
h = 0.5
bit_values_demodulated = sygnal_na_bity(x_calka, y_calka, h)

#zadanie 4
# Sygnał wejściowy do modulacji ASK
bit_values_input = [int(char) for char in string2]

# Znajdowanie indeksów różnic między sygnałem wejściowym a zdemodulowanym sygnałem
bit_differences = [i for i in range(len(bit_values_input)) if bit_values_input[i] != bit_values_demodulated[i]]

# Tworzenie wykresu
plt.figure(figsize=(10, 5))

# Wykres sygnału wejściowego do modulacji ASK
plt.subplot(2, 1, 1)
plt.plot(range(len(bit_values_input)), bit_values_input, linestyle='-', color='b', label='Wejście do modulacji')
plt.title('Wektor bitowy - Sygnał wejściowy do modulacji')
plt.xlabel('Czas [Tb]')
plt.ylabel('Wartość bitu')
plt.grid(True)
plt.legend()

# Wykres zdemodulowanego sygnału
plt.subplot(2, 1, 2)
plt.plot(range(len(bit_values_demodulated)), bit_values_demodulated, linestyle='-', color='r', label='Zdemodulowany sygnał')
plt.title('Wektor bitowy - Zdemodulowany sygnał')
plt.xlabel('Czas [Tb]')
plt.ylabel('Wartość bitu')
plt.grid(True)
plt.legend()

# Zaznaczenie różnic na wykresie zdemodulowanego sygnału
for bit_difference in bit_differences:
    plt.axvline(x=bit_difference, color='gray', linestyle='--')

plt.tight_layout()
plt.show()
plt.savefig("porownania_ask.png")

# Porównanie sygnału wejściowego zdemodulowanego z sygnałem modulacyjnym dla PSK
plt.plot(xp, yp, label='Sygnał wejściowy')
plt.plot(xp_calka, yp_calka, label='Sygnał zdemodulowany')
plt.xlabel('Czas')
plt.ylabel('Amplituda')
plt.title('Porównanie sygnału wejściowego zdemodulowanego z sygnałem modulacyjnym (PSK)')
plt.legend()
plt.grid(True)
plt.show()
plt.savefig("porownanie_psk.png")

# Porównanie sygnału wejściowego zdemodulowanego z sygnałem modulacyjnym dla FSK
plt.plot(xf, yf, label='Sygnał wejściowy')
plt.plot(xf_calka, yf_calka, label='Sygnał zdemodulowany')
plt.xlabel('Czas')
plt.ylabel('Amplituda')
plt.title('Porównanie sygnału wejściowego zdemodulowanego z sygnałem modulacyjnym (FSK)')
plt.legend()
plt.grid(True)
plt.show()
plt.savefig("porownanie_fsk.png")