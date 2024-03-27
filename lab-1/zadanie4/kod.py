import matplotlib.pyplot as plt
import math

#zad 4
def b(t, max):
    suma = 0
    for h in range(1, max):
        suma+=(math.sin(math.pi*t*(h**2*math.sin(h))))/7*h
    return suma

Tc = 1 #Tc  - czas tworzenia sugnału [s]
fs = 22050 #fs - częstotliwość próbowkoania [Hz = 1/s]

N = Tc*fs #N - liczba próbek Tc*fs
#fmax = fs/2

x = []
y = []
for n in range(0, N):
    t=n/fs
    x.append(t)
    w=b(t, 2)
    y.append(w)

plt.plot(x, y, 'm')
plt.title("Wykres b1(t)")
plt.xlabel("t [sekunda]")
plt.ylabel("Sygnał")
plt.show()
plt.savefig("b1")

x = []
y = []
for n in range(0, N):
    t=n/fs
    x.append(t)
    w=b(t, 4)
    y.append(w)

plt.plot(x, y, 'm')
plt.title("Wykres b2(t)")
plt.xlabel("t [sekunda]")
plt.ylabel("Sygnał")
plt.show()
plt.savefig("b2")

x = []
y = []
for n in range(0, N):
    t=n/fs
    x.append(t)
    w=b(t, 8)
    y.append(w)

plt.plot(x, y, 'm')
plt.title("Wykres b3(t)")
plt.xlabel("t [sekunda]")
plt.ylabel("Sygnał")
plt.show()
plt.savefig("b3")

