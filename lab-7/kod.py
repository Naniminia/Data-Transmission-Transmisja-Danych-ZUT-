import numpy as np
import matplotlib.pyplot as plt
import math


#zad 1
x = [1, 1, 0, 1]
string1 = 'Do testow'

def zamiana(string1):
    string3 = ''
    for i in string1:
        string3 += bin(ord(i))[2:]
    return string3

def zamiana2(string1):
    string3 = []
    for i in string1:
        string3.append(bin(ord(i))[2:])
    return string3

string2 = zamiana(string1)
Tb = 1
W = 2
fn = W * pow(Tb, -1)
Tc = Tb * len(string2)
fs = 200
fi = 180
f = 1000
N = int(Tc * fs)
fn1 = (W + 1) / Tb
fn2 = (W + 2) / Tb
def HammingKoder(x):
    x1 = np.zeros(7, int)
    x1[2]=x[0]
    x1[4]=x[1]
    x1[5]=x[2]
    x1[6]=x[3]
    a = ((x1[2]+x1[4]+x1[6])%2)
    b = ((x1[2]+x1[5]+x1[6])%2)
    c = ((x1[4]+x1[5]+x1[6])%2)
    x1[0]=a
    x1[1]=b
    x1[3]=c
    return x1

def kluczowanieASK(podaj, fs, fn, Tb):
    A1 = 0
    A2 = 1
    wyjscie1 = []
    wyjscie2 = []

    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = (int(t / Tb))%2
        if podaj[indeks] == "0":
            wyjscie2.append(A1 * (math.sin(2 * math.pi * fn * t)))
        else:
            wyjscie2.append(A2 * (math.sin(2 * math.pi * fn * t)))
    return wyjscie1, wyjscie2

def calkowanie(x, y, Tb):
    wynik = []
    suma = 0
    for i in range(len(x)):
        suma += y[i]
        wynik.append(suma * Tb)
    return x, wynik

def porownaj_z_h(x_calka, y_calka, h):
    x_wynik = []
    y_wynik = []
    for i in range(len(x_calka)):
        if y_calka[i] < h:
            x_wynik.append(x_calka[i])
            y_wynik.append(y_calka[i])
    return x_wynik, y_wynik

def HammingDekoder(x1):
    x2=np.zeros(4, int)
    x2[0]=x1[2]
    x2[1]=x1[4]
    x2[2]=x1[5]
    x2[3]=x1[6]
    x1prim = (x1[2]+x1[4]+x1[6])%2
    x1prim2 = ((x1[2]+x1[5]+x1[6])%2)
    x1prim4 = ((x1[4]+x1[5]+x1[6])%2)
    x1daszek = (x1[0] + x1prim)%2
    x2daszek = ((x1[1] + x1prim2)%2)
    x4daszek = ((x1[3] + x1prim4)%2)
    S = ((x1daszek*pow(2,0)) + (x2daszek*pow(2,1)) + (x4daszek*pow(2,2)))
    return x2, S

def modelCyfrowy():
    #etap 1
    #koder nadmiarowy
    model1 = HammingKoder(string2)
    print(model1)
    print(string2)
    # reszta = len(string1) %7
    # print(reszta)
    #kontrolne = HammingKoder(x) do sprawdzenia, czy koder nie działa tak samo w każdym przypadku
    #print(model1)
    #print(kontrolne)

    #etap 2
    #modulator
    model2x, model2y = kluczowanieASK(model1, fs, fn, Tb)
    #print(model2x, model2y)
    # x, y = kluczowanieASK(model1, fs, fn, Tb)

    #etap 3
    #demodulator
    model3x, model3y = calkowanie(model2x, model2y, Tb)
    model3x, model3y = porownaj_z_h(model3x, model3y, Tb)

    #etap 4
    #dekoder
    y4 = HammingDekoder(model3y)
    print("Przed:", model1)
    print("Po   : ", y4)

modelCyfrowy()