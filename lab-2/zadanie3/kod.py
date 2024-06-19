import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from time import time
import cmath
import math
from functools import partial


def dft(y, N):
    wyjscie = []
    for k in range(N):
        wynik = 0
        for n in range(N):
            e = cmath.exp((-1j * 2 * math.pi * k * n) / N)
            wynik += y[n] * e
        wyjscie.append(wynik)
    return wyjscie

def fft(y, N):
    return np.fft.fft(y, N)

def M(y, N):
    przyklad = dft(y, N)
    return [np.abs(przyklad[k]) for k in range(int(N / 2))]

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
    if callable(f):
        f_vectorized = np.vectorize(f)
        y = np.sin(2 * np.pi * f_vectorized(x))
    else:
        y = np.sin(2 * np.pi * f * x)
    return x, y

Tc = 3.0
fs = 500
f = 1000
N = int(Tc * fs)

def f2(x):
    f = 10
    teta = math.pi / 2
    return (math.cos(2 * math.pi * x * f + teta)) * math.cos(2.5 * x ** 0.2 * math.pi)

def y1(x):
    return (f2(x) * x * 3) / 3

def z1(x):
    return (1.92 * (math.cos(3 * math.pi * (x / 2)) + math.cos(y1(x) ** 2 / (8 * f2(x) + 3) * x)))

def v1(x):
    return (y1(x) * z1(x) / (f2(x) + 2)) * math.cos(7.2 * math.pi * x) + math.sin(math.pi * x ** 2)

def u(t):
    if (t >= 0) and (t < 1.8):
        return (math.sin(12 * math.cos(math.pi * t) * math.pi * t) + t ** 2)
    elif (t >= 1.8) and (t < 2.3):
        return (3 * (t - 1.7) * math.sin(3 * math.pi * t) * math.cos(20 * t ** 2))
    elif (t >= 2.3) and (t < 3):
        return (((t ** 3) / 16) * math.sin(8 * math.pi * t))
    elif (t >= 3) and (t < 3.5):
        return (math.log(t, 2) / (2 + math.sin(4 * math.pi * t)))

def b(t, max):
    suma = 0
    for h in range(1, max):
        suma += (math.sin(math.pi * t * (h ** 2 * math.sin(h)))) / 7 * h
    return suma

Tc_f2 = 3.0
Tc_y1 = 6.0

N = int(Tc_f2 * fs)

x, y = wywolanie(Tc_f2, fs, N, f2)
M(y, N)
y3 = Mprim(y, N)
x3 = skala(fs, N)

plt.plot(x3, y3)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji f2')
plt.show()

xy, yy = wywolanie(Tc_f2, fs, N, y1)
M(yy, N)
y2 = Mprim(yy, N)
x1 = skala(fs, N)

plt.plot(x1, y2)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji y1')
plt.show()

xz, yz = wywolanie(Tc_f2, fs, N, z1)
M(yz, N)
y4 = Mprim(yz, N)
x4 = skala(fs, N)
plt.plot(x4, y4)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji z1')
plt.show()

xv, yv = wywolanie(Tc_f2, fs, N, v1)
M(yv, N)
y5 = Mprim(yv, N)
x5 = skala(fs, N)
plt.plot(x5, y5)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji v1')
plt.show()

xu, yu = wywolanie(Tc_f2, fs, N, u)
M(yu, N)
y6 = Mprim(yu, N)
x6 = skala(fs, N)

plt.plot(x6, y6)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji u')
plt.show()

xb1, yb1 = wywolanie(Tc_f2, fs, N, partial(b, max=2))
M(yb1, N)
y7 = Mprim(yb1, N)
x7 = skala(fs, N)
plt.plot(x7, y7)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji b1 (dla max =2)')
plt.show()

xb2, yb2 = wywolanie(Tc_f2, fs, N, partial(b, max=4))
M(yb2, N)
y8 = Mprim(yb2, N)
x8 = skala(fs, N)
plt.plot(x8, y8)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji b2 (dla max=4)')
plt.show()

xb3, yb3 = wywolanie(Tc_f2, fs, N, partial(b, max=8))
M(yb3, N)
y9 = Mprim(yb3, N)
x9 = skala(fs, N)
plt.plot(x9, y9)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji b3 (dla max=8)')
plt.show()
