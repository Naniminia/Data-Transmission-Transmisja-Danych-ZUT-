import matplotlib.pyplot as plt
import cmath
import math
import numpy as np

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

#zadanie 1
def sinus(x, y, fn, N):
    A = 1
    wynik = []
    x = []
    for n in range(N):
        t = n / fs
        x.append(t)
        wynik.append(A*math.sin(2*math.pi*fn*t))
    return x, wynik


#do popraawy
def calkowanie(x, y, fn): #wykorzystując metodę trapezów
    x = []
    y = []
    h = (y - x) / N #trzeba poprawić coś z tą linijką
    sumaT = 0
    for i in range(N):
        fx = x+h*i
        sumaT = sumaT + h*(sinus(x, y, fn, fx)+sinus(x, y, fn, fx+h))/2
    return sumaT

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
x1, y1, = sinus(x, y, fn, N)
plt.plot(x, y, 'm')
plt.show()
plt.plot(x1, y1, 'm')
plt.show()

