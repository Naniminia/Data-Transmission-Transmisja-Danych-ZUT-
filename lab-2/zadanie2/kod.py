import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from time import time
import cmath
import math


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
plt.show()
