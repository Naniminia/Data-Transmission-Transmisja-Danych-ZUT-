import matplotlib.pyplot as plt
import cmath
import math

#Przygotowanie do zadań, to było w uwagach
string1 = 'ABC'
def zamiana(string1): #orde zmiania na ASCII, bin na binarny
    return [ord(x) for x in string1], [bin(ord(x))[2::] for x in string1]

print("Wartosc: ", zamiana(string1))

#zad 1
string2 = zamiana(string1)
Tb = 1 #czas trwania pojedynczego bitu [sekundy]
W = 1 #liczba całkowita określa docelową częstotliwość (po wykorzystaniu wzoru na dole)
fn = W*pow(Tb, -1) #częśtotliwości
Tc = Tb*len(string2) #czas próbkowania w sekudnach
fs = 500 #częstotliwość próbkowania musi być większa lub równa 2*(max(fn, fm)
fi = 180
f = 1000 #częstotliwość
N = int(Tc * fs)


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
       # wynik = 0
        if string2[indeks] == '1':
           # wynik = A2*math.sin(2*math.pi*fn*t)
           # wyjscie1.append(wynik)
            wyjscie2.append(A2*(math.sin(2*math.pi*fn*t)))
        else:
            wyjscie2.append(A1*(math.sin(2 * math.pi * fn * t)))
            # wyjscie1.append(wynik)
    return wyjscie1, wyjscie2

x, y = kluczowanieASK(string2, fs, fn, Tb)
plt.plot(x, y)
plt.show()