import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from time import time
import cmath
import math

def dft(y, N):
    wyjscie = []
    #wynik = 0 daje zupełnie inny wynik/wykres
    for k in range(N):
        wynik = 0
        for n in range(N):
            e = cmath.exp((-1j * 2 * math.pi * k * n) / N)
            wynik += y[n] * e
        wyjscie.append(wynik)
    return wyjscie


def M(y, N):
    przyklad = dft(y, N)
    return [np.abs(przyklad[k]) for k in range(int(N / 2))] #dla liczb zespolonych abs zwraca moduł a dla zwykłych wartość bezwzględną

def Mprim(y, N):
    przyklad2 = M(y, N)
    wyjscie2 = []
    for k in range(int(N / 2)):
        wyjscie2.append(10 * np.log10(przyklad2[k]))
    return wyjscie2

def skala(fs, N):
    return [k * fs / N for k in range(int(N / 2))]

def wywolanie(Tc, fs, N, f):
    x = np.linspace(0, Tc, N)
    y = np.sin(2 * np.pi * f * x)
    return x, y


Tc = 3.0 #czas próbkowania w sekudnach
fs = 100 #częstotliwość próbkowania
fi = 180
f = 1000 #częstotliwość
N = int(Tc * fs)

# Generowanie danych
x, y = wywolanie(Tc, fs, N, f)

# Obliczanie i rysowanie widma
wyjscie3 = skala(fs, N)
wyjscie1 = M(y, N)

plt.plot(wyjscie3, wyjscie1)
plt.title("widmo")
plt.xlabel("czestotliwosc")
plt.ylabel("amplituda")
plt.grid(True)
plt.savefig("Widmo")
plt.show()
