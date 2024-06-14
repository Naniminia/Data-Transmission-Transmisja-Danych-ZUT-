import matplotlib.pyplot as plt
import cmath
import math
import numpy as np

#Przygotowanie do zadań, to było w uwagach
string1 = 'ABC'
def zamiana(string1): #orde zmiania na ASCII, bin na binarny
    string3 = ''
    for i in (string1):
        string3 += bin(ord(i))[2:]
    return string3

print("Wartosc: ", zamiana(string1))

#zad 1
string2 = zamiana(string1)
Tb = 1 #czas trwania pojedynczego bitu [sekundy]
W = 2 #liczba całkowita określa docelową częstotliwość (po wykorzystaniu wzoru na dole)
fn = W*pow(Tb, -1) #częśtotliwości
Tc = Tb*len(string2) #czas próbkowania w sekudnach
fs = 200 #częstotliwość próbkowania musi być większa lub równa 2*(max(fn, fm)
fi = 180
f = 1000 #częstotliwość
N = int(Tc * fs)
fn1 = (W+1)/Tb
fn2 = (W+2)/Tb

def dft(y, N):
    wyjscie = []
    for k in range(N):
        wynik = 0
        for n in range(N):
            wynik += y[n] * cmath.exp((-1j * 2 * math.pi * k * n) / N)
        wyjscie.append(wynik)
    return wyjscie

def M(y, N):
    przyklad = dft(y, N)
    wyjscie1 = []
    for k in range(int(N / 2)):
        wyjscie1.append(np.sqrt((np.real(przyklad[k])) ** 2 + (np.imag(przyklad[k])) ** 2))
    return wyjscie1

def Mprim(y, N):
    przyklad2 = M(y, N)
    wyjscie2 = []
    for k in range(int(N / 2)):
        wyjscie2.append(10 * np.log10(przyklad2[k]))
    return wyjscie2
def skala(fs, N):
    wyjscie3 = []
    for k in range(int(N / 2)):
        wyjscie3.append(k * fs / N)
    return wyjscie3

def wywolanie(Tc, fs, N, funkcja):
    x = []
    y = []
    for n in range(0, N):
        t = n / fs
        x.append(t)
        w = funkcja(t)
        y.append(w)
    return x, y

def szerokoscPasma(x, y, dB):
    wektorNaY = np.array(y)
    maksymalneY = wektorNaY.max()
    wektorNaX = np.array(x)

    min1 = 1
    max1 = 0
    for i in range(len(wektorNaX)):
        if y[i] > (maksymalneY - dB):
            if x[i] > max1:
                max1 = x[i]
            elif x[i] < min1:
                min1 = x[i]
    Pasmo = max1 - min1
    print("Wartość szerokości pasma o dB równym", dB, "wynosi", Pasmo)

def kluczowanieASK(string2, fs, fn, Tb):
    A1 = 0 #dla 0
    A2 = 1 #dla 1
    wyjscie1 = []
    wyjscie2 = []

    #Tc = Tb*len(string1)
    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t/Tb)
       # print(string2[0])

       # wynik = 0
        if string2[indeks] == '0':
           # wynik = A2*math.sin(2*math.pi*fn*t)
           # wyjscie1.append(wynik)
            wyjscie2.append(A1*(math.sin(2*math.pi*fn*t)))
           # print("kaczka")
        else:
            wyjscie2.append(A2*(math.sin(2 * math.pi * fn * t)))
            # wyjscie1.append(wynik)
            #print("piesek")
    return wyjscie1, wyjscie2

x, y = kluczowanieASK(string2, fs, fn, Tb)
plt.plot(x, y, 'm')
plt.show()
# plt.savefig('za.png')

M(y, N)
y = Mprim(y, N)
x = skala(fs, N)
plt.plot(x, y, 'm')
plt.xlabel("częstotliwość")
plt.ylabel("amplituda")
szerokoscPasma(x, y, 3)
szerokoscPasma(x, y, 6)
szerokoscPasma(x, y, 12)
plt.show()
# plt.savefig('za_widmo.png')

def KluczowaniePSK(string2, fs, fn, Tb):
    wyjscie1 = []
    wyjscie2 = []

    # Tc = Tb*len(string1)
    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t / Tb)

        # wynik = 0
        if string2[indeks] == '0':
            # wynik = A2*math.sin(2*math.pi*fn*t)
            # wyjscie1.append(wynik)
            wyjscie2.append(math.sin(2 * math.pi * fn * t))
        # print("kaczka")
        else:
            wyjscie2.append(math.sin(2 * math.pi * fn * t + math.pi))
            # wyjscie1.append(wynik)
            # print("piesek")
    return wyjscie1, wyjscie2

x1, y1 = KluczowaniePSK(string2, fs, fn, Tb)
plt.plot(x1, y1, 'm')
# plt.show()
# plt.savefig('zp.png')

M(y1, N)
y1 = Mprim(y1, N)
x1 = skala(fs, N)
plt.plot(x1, y1)
szerokoscPasma(x1, y1, 3)
szerokoscPasma(x1, y1, 6)
szerokoscPasma(x1, y1, 12)
# plt.show()
# plt.savefig('zp_widmo.png')

def KluczowanieFSK(string2, fs, fn1, fn2, Tb):
    wyjscie1 = []
    wyjscie2 = []

    # Tc = Tb*len(string1)
    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t / Tb)

        # wynik = 0
        if string2[indeks] == '0':
            # wynik = A2*math.sin(2*math.pi*fn*t)
            # wyjscie1.append(wynik)
            wyjscie2.append(math.sin(2 * math.pi * fn1 * t))
        # print("kaczka")
        else:
            wyjscie2.append(math.sin(2 * math.pi * fn2 * t ))
            # wyjscie1.append(wynik)
            # print("piesek")
    return wyjscie1, wyjscie2

x2, y2 = KluczowaniePSK(string2, fs, fn, Tb)
plt.plot(x2, y2, 'm')
# plt.show()
# plt.savefig('zf.png')

M(y2, N)
y2 = Mprim(y2, N)
x2 = skala(fs, N)
plt.plot(x2, y2)

szerokoscPasma(x2, y2, 3)
szerokoscPasma(x2, y2, 6)
szerokoscPasma(x2, y2, 12)
# plt.show()
# plt.savefig('zf_widmo.png')