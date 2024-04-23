import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import cmath
import math

Tc = 3.0
fs = 10000
fi = 180
f = 1000
N = int(Tc * fs)

x = np.linspace(0, Tc, N)

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



