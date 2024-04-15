import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from time import time
import cmath
import math


Tc = 3.0
fs = 100
fi = 180
f = 1000
N = math.floor(Tc * fs)

x = np.linspace(0, Tc, N)
y = []

def dft(y, N):
    wyjscie =[]
    for k in range(int(N/2)):
        wynik = 0;
        for n in range(N):
            wynik += y[n]*cmath.exp((-1j*2*math.pi*k*n)/N)
        wyjscie.append(wynik)
    return wyjscie

#plt.plot(dft(np.sin(2*np.pi*f*x)))
#plt.show()

#zad 2
def M(y, N):
    przyklad = dft(y, N)
    wyjscie1 = []
    for k in range(int(N / 2)):
        wyjscie1.append(np.sqrt((np.real(przyklad)) ** 2 + (np.imag(przyklad)) ** 2))
    return wyjscie1

def Mprim(y, N):
    przyklad2 = M(y, N)
    wyjscie2 = []
    for k in range(int(N/2)):
        wyjscie2 = 10*math.log10(przyklad2)
    return wyjscie2

def skala(y, N):
    wyjscie3 = []
    for k in range(int(N/2)):
        wyjscie3 = x*fs/N
    return wyjscie3

def wywolanie(Tc, fs, N, f):
    x1 = []
    y = []
    N = int(Tc*fs)
    for t in range(0, N):
        t=N/fs
        x.append(t)
        w=dft(t)
        y.append(w)
    return x1, y

skala1 = skala(fs, N)
dana = M(fs, N)

plt.plot(skala1, dana)
plt.show()
plt.savefig("widmo")