import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from time import time
import cmath
import math
from functools import partial

Tc = 3.0 #czas próbkowania w sekudnach
fs = 500 #częstotliwość próbkowania musi być większa lub równa 2*(max(fn, fm)
fi = 180
f = 1000 #częstotliwość
N = int(Tc * fs)
fn = 10
fm = 2
def m(t):
    return math.sin(2*math.pi*t*fm)

#sygnał zmodulowanyu amplitudowo:
def za(t, ka):
    return ((ka*m(t)+1)*math.cos(2*math.pi*fn*t))

#sygbał zmodulowany kątowo
def zp(t, kp): #modulacja fazy
    return math.cos(2*math.pi*t*fn+(kp*m(t)))
def zf(t, kf): #modulacja częstotliwości
    return math.cos(2*math.pi*fn*t+(kf/fm)*m(t))

#zadanie 1 i 2
#k - głębokość modulacji
def wywolanie(Tc, fs, N, funkcja):
    x = []
    y = []
    for n in range(0, N):
        t = n / fs
        x.append(t)
        w = funkcja(t)
        y.append(w)
    return x, y

x0, y0 = wywolanie(Tc, fs, N, m)


# x1, y1 = wywolanie(Tc, fs, N, partial(za, ka=0.5))
# plt.plot(x1, y1)
# plt.plot(x0, y0)
# plt.show()
# plt.savefig('za_a.png')
#
# x2, y2 = wywolanie(Tc, fs, N, partial(za, ka=6))
# plt.plot(x0, y0)
# plt.plot(x2, y2)
# plt.show()
# plt.savefig('za_b.png')
#
# x3, y3 = wywolanie(Tc, fs, N, partial(za, ka=26))
# plt.plot(x0, y0)
# plt.plot(x3, y3)
# plt.show()
# plt.savefig('za_c.png')
#
# x4, y4 = wywolanie(Tc, fs, N, partial(zp, kp=0.5))
# plt.plot(x0, y0)
# plt.plot(x4, y4, 'm')
# plt.show()
# plt.savefig('zp_a.png')
#
# x5, y5 = wywolanie(Tc, fs, N, partial(zp, kp=math.pi/2))
# plt.plot(x0, y0)
# plt.plot(x5, y5, 'm')
# plt.show()
# plt.savefig('zp_b.png')
#
# x6, y6 = wywolanie(Tc, fs, N, partial(zp, kp=4*math.pi))
# plt.plot(x0, y0)
# plt.plot(x6, y6, 'm')
# plt.show()
# plt.savefig('zp_c.png')
#
# x7, y7 = wywolanie(Tc, fs, N, partial(zf, kf=0.5))
# plt.plot(x0, y0)
# plt.plot(x7, y7, 'g')
# plt.show()
# plt.savefig('zf_a.png')
#
# x8, y8 = wywolanie(Tc, fs, N, partial(zf, kf=math.pi/3))
# plt.plot(x0, y0)
# plt.plot(x8, y8, 'g')
# plt.show()
# plt.savefig('zf_b.png')
#
# x9, y9 = wywolanie(Tc, fs, N, partial(zf, kf=5*math.pi))
# plt.plot(x0, y0)
# plt.plot(x9, y9, 'g')
# plt.show()
# plt.savefig('zf_c.png')

#zadanie 3
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

# x, y = wywolanie(Tc, fs, N, partial(za, ka=0.5))
# M(y, N)
# y1 = Mprim(y, N)
# x1 = skala(fs, N)
# plt.plot(x1, y1)
# plt.show()
# plt.savefig('za_a_widmo.png')
#
# x, y = wywolanie(Tc, fs, N, partial(za, ka=6))
# M(y, N)
# y2 = Mprim(y, N)
# x2 = skala(fs, N)
# plt.plot(x2, y2)
# plt.show()
# plt.savefig('za_b_widmo.png')
#
# x, y = wywolanie(Tc, fs, N, partial(za, ka=26))
# M(y, N)
# y3 = Mprim(y, N)
# x3 = skala(fs, N)
# plt.plot(x3, y3)
# plt.show()
# plt.savefig('za_c_widmo.png')
#
# x, y = wywolanie(Tc, fs, N, partial(zp, kp=0.5))
# M(y, N)
# y4 = Mprim(y, N)
# x4 = skala(fs, N)
# plt.plot(x4, y4, 'm')
# plt.show()
# plt.savefig('zp_a_widmo.png')
#
# x, y = wywolanie(Tc, fs, N, partial(zp, kp=math.pi/2))
# M(y, N)
# y5 = Mprim(y, N)
# x5 = skala(fs, N)
# plt.plot(x5, y5, 'm')
# plt.show()
# plt.savefig('zp_b_widmo.png')
#
# x, y = wywolanie(Tc, fs, N, partial(zp, kp=4*math.pi))
# M(y, N)
# y6 = Mprim(y, N)
# x6 = skala(fs, N)
# plt.plot(x6, y6, 'm')
# plt.show()
# plt.savefig('zp_c_widmo.png')
#
# x, y = wywolanie(Tc, fs, N, partial(zf, kf=0.12))
# M(y, N)
# y7 = Mprim(y, N)
# x7 = skala(fs, N)
# plt.plot(x7, y7, 'g')
# plt.show()
# plt.savefig('zf_a_widmo.png')
#
# x, y = wywolanie(Tc, fs, N, partial(zf, kf=math.pi/3))
# M(y, N)
# y8 = Mprim(y, N)
# x8 = skala(fs, N)
# plt.plot(x8, y8, 'g')
# plt.show()
# plt.savefig('zf_b_widmo.png')
#
# x, y = wywolanie(Tc, fs, N, partial(zf, kf=5*math.pi))
# M(y, N)
# y9 = Mprim(y, N)
# x9 = skala(fs, N)
# plt.plot(x9, y9, 'g')
# plt.show()
# plt.savefig('zf_c_widmo.png')

#zad4
#tylko tych z widma, ale 9
def szerokoscPasma(x, y, dB):
    wektorNaY = np.array(y)
    maksymalneY = wektorNaY.max()
    wektorNaX = np.array(x)

    min1 = 10
    max1 = 0
    for i in range(len(wektorNaX)):
        if y[i] > (maksymalneY - dB):
            if x[i] > max1:
                max1 = x[i]
            elif x[i] < min1:
                min1 = x[i]
    Pasmo = max1 - min1
    print("Wartość szerokości pasma o dB równym", dB, "wynosi", Pasmo)


x, y = wywolanie(Tc, fs, N, partial(za, ka=0.5))
M(y, N)
y1 = Mprim(y, N)
x1 = skala(fs, N)
plt.plot(x1, y1)
szerokoscPasma(x1, y1, 3)
szerokoscPasma(x1, y1, 6)
szerokoscPasma(x1, y1, 12)
#plt.show()
#plt.savefig('za_a_widmo.png')

x, y = wywolanie(Tc, fs, N, partial(za, ka=6))
M(y, N)
y2 = Mprim(y, N)
x2 = skala(fs, N)
plt.plot(x2, y2)
szerokoscPasma(x2, y2, 3)
szerokoscPasma(x2, y2, 6)
szerokoscPasma(x2, y2, 12)
#plt.show()
# plt.savefig('za_b_widmo.png')
#
x, y = wywolanie(Tc, fs, N, partial(za, ka=26))
M(y, N)
y3 = Mprim(y, N)
x3 = skala(fs, N)
plt.plot(x3, y3)
szerokoscPasma(x3, y3, 3)
szerokoscPasma(x3, y3, 6)
szerokoscPasma(x3, y3, 12)
#plt.show()
# plt.savefig('za_c_widmo.png')
#
x, y = wywolanie(Tc, fs, N, partial(zp, kp=0.5))
M(y, N)
y4 = Mprim(y, N)
x4 = skala(fs, N)
plt.plot(x4, y4, 'm')
szerokoscPasma(x4, y4, 3)
szerokoscPasma(x4, y4, 6)
szerokoscPasma(x4, y4, 12)
# plt.show()
# plt.savefig('zp_a_widmo.png')
#
x, y = wywolanie(Tc, fs, N, partial(zp, kp=math.pi/2))
M(y, N)
y5 = Mprim(y, N)
x5 = skala(fs, N)
plt.plot(x5, y5, 'm')
szerokoscPasma(x5, y5, 3)
szerokoscPasma(x5, y5, 6)
szerokoscPasma(x5, y5, 12)
#plt.show()
# plt.savefig('zp_b_widmo.png')
#
x, y = wywolanie(Tc, fs, N, partial(zp, kp=4*math.pi))
M(y, N)
y6 = Mprim(y, N)
x6 = skala(fs, N)
plt.plot(x6, y6, 'm')
szerokoscPasma(x6, y6, 3)
szerokoscPasma(x6, y6, 6)
szerokoscPasma(x6, y6, 12)
# plt.show()
# plt.savefig('zp_c_widmo.png')
#
x, y = wywolanie(Tc, fs, N, partial(zf, kf=0.12))
M(y, N)
y7 = Mprim(y, N)
x7 = skala(fs, N)
plt.plot(x7, y7, 'g')
szerokoscPasma(x7, y7, 3)
szerokoscPasma(x7, y7, 6)
szerokoscPasma(x7, y7, 12)
# plt.show()
# plt.savefig('zf_a_widmo.png')
#
x, y = wywolanie(Tc, fs, N, partial(zf, kf=math.pi/3))
M(y, N)
y8 = Mprim(y, N)
x8 = skala(fs, N)
plt.plot(x8, y8, 'g')
szerokoscPasma(x8, y8, 3)
szerokoscPasma(x8, y8, 6)
szerokoscPasma(x8, y8, 12)
# plt.show()
# plt.savefig('zf_b_widmo.png')
#
x, y = wywolanie(Tc, fs, N, partial(zf, kf=5*math.pi))
M(y, N)
y9 = Mprim(y, N)
x9 = skala(fs, N)
plt.plot(x9, y9, 'g')
szerokoscPasma(x9, y9, 3)
szerokoscPasma(x9, y9, 6)
szerokoscPasma(x9, y9, 12)
# plt.show()
# plt.savefig('zf_c_widmo.png')