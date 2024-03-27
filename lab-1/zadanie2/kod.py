import matplotlib.pyplot as plt
import math

#zad 1

def f2(x):
    f=1
    teta = math.pi/2
    return (math.cos(2*math.pi*x*f+teta))*math.cos(2.5*t**0.2*math.pi)

def y1(x):
    return (f2(x)*x*3)/3

def z1(x):
   return (1.92*(math.cos(3*math.pi*(x/2))+math.cos(y1(x)**2/(8*f2(x)+3)*x)))


def v1(x):
    return (y1(x)*z1(x)/(f2(x)+2))*math.cos(7.2*math.pi*x)+math.sin(math.pi*x**2)

Tc = 5 #Tc  - czas tworzenia sugnału [s]
fs = 800 #fs - częstotliwość próbowkoania [Hz = 1/s]

N = Tc*fs #N - liczba próbek Tc*fs
#fmax = fs/2
x = []
y = []
for n in range(0, N):
    t=n/fs
    x.append(t)
    w=y1(t)
    y.append(w)

plt.plot(x, y, 'm')
plt.title("Wykres y(t)")
plt.xlabel("t [sekunda]")
plt.ylabel("Sygnał")
plt.show()
plt.savefig("y")

x = []
y = []
for n in range(0, N):
    t=n/fs
    x.append(t)
    w=z1(t)
    y.append(w)

print(x)
print(y)
plt.plot(x, y, 'm')
plt.title("Wykres z(t)")
plt.xlabel("t [sekunda]")
plt.ylabel("Sygnał")
plt.show()
plt.savefig("z")

x = []
y = []
for n in range(0, N):
    t = n / fs
    x.append(t)
    w = v1(t)
    y.append(w)

print(x)
print(y)
plt.plot(x, y, 'm')
plt.title("Wykres v(t)")
plt.xlabel("t [sekunda]")
plt.ylabel("Sygnał")
plt.show()
plt.savefig("v")

