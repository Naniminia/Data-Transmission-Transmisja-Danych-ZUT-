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


Tc = 3.0 #czas próbkowania w sekudnach
fs = 500 #częstotliwość próbkowania
fi = 180
f = 1000 #częstotliwość
N = int(Tc * fs)


def f2(x):
    f=10
    teta = math.pi/2
    return (math.cos(2*math.pi*x*f+teta))*math.cos(2.5*x**0.2*math.pi)
def y1(x):
    return (f2(x)*x*3)/3
def z1(x):
   return (1.92*(math.cos(3*math.pi*(x/2))+math.cos(y1(x)**2/(8*f2(x)+3)*x)))

def v1(x):
    return (y1(x)*z1(x)/(f2(x)+2))*math.cos(7.2*math.pi*x)+math.sin(math.pi*x**2)

def u(t):
    if (t>=0)and(t<1.8):
        return (math.sin(12*math.cos(math.pi*t)*math.pi*t)+t**2)
    elif (t>=1.8)and(t<2.3):
        return (3*(t-1.7)*math.sin(3*math.pi*t)*math.cos(20*t**2))
    elif (t>=2.3)and(t<3):
        return (((t**3)/16)*math.sin(8*math.pi*t))
    elif (t>=3)and(t<3.5):
        return (math.log(t,2)/(2+math.sin(4*math.pi*t)))

def b(t, max):
    suma = 0
    for h in range(1, max):
        suma+=(math.sin(math.pi*t*(h**2*math.sin(h))))/7*h
    return suma

Tc_f2 = 3.0
Tc_y1 = 6.0

x, y = wywolanie(Tc_f2, fs, N, f2)
M(y, N)
y3 = Mprim(y, N)
x3 = skala(fs, N)

plt.plot(x3, y3)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji f2')
plt.show()
plt.savefig('x.png')

x, y = wywolanie(Tc_f2, fs, N, y1)
M(y, N)
y2 = Mprim(y, N)
x1 =skala(fs, N)

plt.plot(x1, y2)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji y1')
plt.show()
plt.savefig('y.png')

x, y = wywolanie(Tc_f2, fs, N, z1)
M(y, N)
y4 = Mprim(y, N)
x4 = skala(fs, N)

plt.plot(x4, y4)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji z1')
plt.show()
plt.savefig('z.png')

x, y = wywolanie(Tc_f2, fs, N, v1)
M(y, N)
y5 = Mprim(y, N)
x5 = skala(fs, N)

plt.plot(x5, y5)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji v1')
plt.show()
plt.savefig('v.png')

x, y = wywolanie(Tc_f2, fs, N, u)
M(y, N)
y6 = Mprim(y, N)
x6 = skala(fs, N)

plt.plot(x6, y6)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji u')
plt.show()
plt.savefig('u.png')

x, y = wywolanie(Tc_f2, fs, N, partial(b, max=2))
M(y, N)
y7 = Mprim(y, N)
x7 = skala(fs, N)

plt.plot(x7, y7)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji b1 (dla max =2)')
plt.show()
plt.savefig('b1.png')

x, y = wywolanie(Tc_f2, fs, N, partial(b, max=4))
M(y, N)
y8 = Mprim(y, N)
x8 = skala(fs, N)

plt.plot(x8, y8)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji b2 (dla max=4)')
plt.show()
plt.savefig('b2.png')

x, y = wywolanie(Tc_f2, fs, N, partial(b, max=8))
M(y, N)
y9 = Mprim(y, N)
x9 = skala(fs, N)

plt.plot(x9, y9)
plt.xlabel('Częstotliwość')
plt.ylabel('Amplituda')
plt.title('Wykres funkcji b3 (dla max=8)')
plt.show()
plt.savefig('b3.png')