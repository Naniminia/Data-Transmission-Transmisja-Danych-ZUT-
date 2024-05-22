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
def calkowanie(x, y, N, Tb): #wykorzystując metodę prostokątów
    wynik = []
    wartosci = 1
    suma = 0
    for i in range(N):
        wynik.append(suma)
        if x[i]>=(Tb*wartosci):
            suma = 0
            wartosci +=1
        else:
            suma = (wartosci*Tb)
    return x, wynik

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
x2, y2 = calkowanie(x, y, N, Tb)
plt.plot(x, y)
plt.show()
plt.savefig('ask_z.png')
plt.plot(x1, y1, 'm')
plt.show()
plt.savefig('ask_x.png')

print("x:", x2)
print("y:", y2)
plt.plot(x2,y2)
plt.show()
plt.savefig('ask_p.png')

# def AbyObliczycH(x, y, N, Tb):
#     suma = 0
#     wynik=0
#     wynik1 = []
#     for i in range(N):
#         wynik1.append(wynik)
#         if  x[i] >= 0:
#             suma+=x[i]
#             print(suma)
#         else:
#             print("kaczuszka, blad")
#         wynik = suma/len(x)
#         return wynik1
#
# MojeH = AbyObliczycH(x2, y2, N, Tb)
# print("H= ", MojeH)

def ASKCT (x, y, N, Tb):
    wyjscie = []
    wynik = []
    for i in range(N):
        if x[i] > 0.56:
            wyjscie = x
            wynik = y
            print("kaczuszka")
        else:
            print("nie ma")
    return wyjscie, wynik

x3, y3 = ASKCT(x2, y2, N, Tb)
plt.plot(x3, y3)
plt.show()
plt.savefig('ask_p.png')

def KluczowaniePSK(string2, fs, fn, Tb):
    wyjscie1 = []
    wyjscie2 = []

    # Tc = Tb*len(string1)
    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t / Tb)

        # wynik = 0
        if string2[indeks] == '0':
            # wynik = A2*math.sin(2*math.pi*fn*t)
            # wyjscie1.append(wynik)
            wyjscie2.append(math.sin(2 * math.pi * fn * t))
        # print("kaczka")
        else:
            wyjscie2.append(math.sin(2 * math.pi * fn * t + math.pi))
            # wyjscie1.append(wynik)
            # print("piesek")
    return wyjscie1, wyjscie2


def PSKCT (x, y, N, Tb):
    wyjscie = []
    wynik = []
    for i in range(N):
        if x[i] < 0:
            wyjscie = x
            wynik = y
            print("kaczuszka")
        else:
            print("nie ma")
    return wyjscie, wynik

xp, yp = KluczowaniePSK(string2, fs, fn, Tb)
xp1, yp1, = sinus(xp, yp, fn, N)
xp2, yp2 = calkowanie(xp, yp, N, Tb)
plt.plot(xp, yp)
plt.show()
plt.savefig('psk_z.png')
plt.plot(xp1, yp1, 'm')
plt.show()
plt.savefig('psk_x.png')

print("x:", xp2)
print("y:", yp2)
plt.plot(xp2,yp2)
plt.show()
plt.savefig('psk_p.png')
xp3, yp3 = PSKCT(xp2, yp2, N, Tb)
plt.plot(xp3, yp3)
plt.show()
plt.savefig('psk_c.png')


#uklad FSK
def KluczowanieFSK(string2, fs, fn1, fn2, Tb):
    wyjscie1 = []
    wyjscie2 = []

    # Tc = Tb*len(string1)
    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t / Tb)

        # wynik = 0
        if string2[indeks] == '0':
            # wynik = A2*math.sin(2*math.pi*fn*t)
            # wyjscie1.append(wynik)
            wyjscie2.append(math.sin(2 * math.pi * fn1 * t))
        # print("kaczka")
        # else:
        #     wyjscie2.append(math.sin(2 * math.pi * fn2 * t ))
        #     # wyjscie1.append(wynik)
        #     # print("piesek")
    return wyjscie1, wyjscie2

def KluczowanieFSK1(string2, fs, fn1, fn2, Tb):
    wyjscie1 = []
    wyjscie2 = []

    # Tc = Tb*len(string1)
    for n in range(0, N):
        t = n / fs
        wyjscie1.append(t)
        indeks = int(t / Tb)

        # wynik = 0
        if string2[indeks] == '1':
            # wynik = A2*math.sin(2*math.pi*fn*t)
            # wyjscie1.append(wynik)
            wyjscie2.append(math.sin(2 * math.pi * fn2 * t))
        # print("kaczka")
        # else:
        #     wyjscie2.append(math.sin(2 * math.pi * fn2 * t ))
        #     # wyjscie1.append(wynik)
        #     # print("piesek")
    return wyjscie1, wyjscie2

fn1 = 1
fn2 = 2
xf1, yf1 = KluczowanieFSK(string2, fs, fn1, fn2, Tb)
# print("x: ", xf1)
# print("y: ", yf1)
xf2, yf2, = sinus(xf1, yf1, fn, N)
xf3, yf3 = calkowanie(xf2, yf2, N, Tb)
plt.plot(xf1, yf1)
plt.show()
plt.savefig('fsk_z.png')
plt.plot(xf2, xf2)
plt.show()
plt.savefig('fsk_x1.png')
xff2, yff2 = KluczowanieFSK1(string2, fs, fn1, fn2, Tb)
# print("Druga wersja:")
# print("x1: ", xf2)
# print("y1: ", yf2)
xff3, yff3, = sinus(xff2, yff2, fn, N)
xff4, yff4 = calkowanie(xff3, yff3, N, Tb)
plt.plot(xff2, yff2)
plt.show()
plt.savefig('fsk_x2.png')
plt.plot(xf2, xf2)
plt.show()
plt.savefig('fsk_p2.png')
xcalkowane, ycalkowane = calkowanie(xf1, yf1, N, Tb)
xcal1, ycal1 = calkowanie(xf2, yf2, N, Tb)
sumax = []
sumay = []
for i in range (N):
    sumax.append(xcalkowane[i])
    sumax.append(xcal1[i])
    sumay.append(ycalkowane)
    sumay.append(ycal1)


print("Suma: ", sumax)
#print("Xcal1: ", xcal1)
print("Suma y: ", sumay)

def FSKCT (x, y, N, Tb):
    wyjscie = []
    wynik = []
    for i in range(N):
        if x[i] > 0:
            wyjscie = x
            wynik = y
           # print("kaczuszka")
    return wyjscie, wynik

xf3, yf3 = FSKCT(sumax, sumay, N, Tb)
plt.plot(xf3, yf3)
plt.show()

print(x2)
print(y2)