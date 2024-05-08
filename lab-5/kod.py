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
def sinus(fn, t):
    return math.sin(2*math.pi*fn*t)

def calkowanie(x, y, N, funkcja): #wykorzystując metodę trapezów
    x = []
    y = []
    h = (y-x)/N
    sumaT = 0

    for i in range(N):
        fx = x+h*i
        sumaT = sumaT + h*(funkcja(fx)+funkcja(fx+h))/2
    return sumaT
