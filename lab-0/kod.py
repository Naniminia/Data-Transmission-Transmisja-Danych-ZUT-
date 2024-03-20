import matplotlib.pyplot as plt
import math
def f(x):
    return 2*x**3+0.5*(x + 5)


Tc = 5 #Tc  - czas tworzenia sugnału [s]
fs = 8 #fs - częstotliwość próbowkoania [Hz = 1/s]

N = Tc*fs #N - liczba próbek Tc*fs
#fmax = fs/2
x = []
y = []
for n in range(0, N):
    t=n/fs
    x.append(t)
    w=f(t)
    y.append(w)

print(x)
print(y)
plt.plot(x, y, 'm')
plt.title("Wykres f(x)")
plt.xlabel("t [sekunda]")
plt.ylabel("Sygnał")
plt.show()
plt.savefig("f")