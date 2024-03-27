import matplotlib.pyplot as plt
import math

#zad 1

def f2(x):
    f=1
    teta = math.pi/2
    return (math.cos(2*math.pi*x*f+teta))*math.cos(2.5*t**0.2*math.pi)


Tc = 5 #Tc  - czas tworzenia sugnału [s]
fs = 10000 #fs - częstotliwość próbowkoania [Hz = 1/s]

N = Tc*fs #N - liczba próbek Tc*fs
#fmax = fs/2
x = []
y = []
for n in range(0, N):
    t=n/fs
    x.append(t)
    w=f2(t)
    y.append(w)

print(x)
print(y)
plt.plot(x, y, 'm')
plt.title("Wykres f(x)")
plt.xlabel("t [sekunda]")
plt.ylabel("Sygnał")
plt.show()
plt.savefig("f")

#zad 2
