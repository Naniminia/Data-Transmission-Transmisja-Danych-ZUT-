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

Tc = 3 #Tc  - czas tworzenia sugnału [s]
fs = 9000 #fs - częstotliwość próbowkoania [Hz = 1/s]

N = Tc*fs #N - liczba próbek Tc*fs
#fmax = fs/2

def u(t):
    if (t>=0)and(t<1.8):
        return (math.sin(12*math.cos(math.pi*t)*math.pi*t)+t**2)
    elif (t>=1.8)and(t<2.3):
        return (3*(t-1.7)*math.sin(3*math.pi*t)*math.cos(20*t**2))
    elif (t>=2.3)and(t<3):
        return (((t**3)/16)*math.sin(8*math.pi*t))
    elif (t>=3)and(t<3.5):
        return (math.log(t,2)/(2+math.sin(4*math.pi*t)))

x = []
y = []
for n in range(0, N):
    t=n/fs
    x.append(t)
    w=u(t)
    y.append(w)

plt.plot(x, y, 'm')
plt.title("Wykres u(t)")
plt.xlabel("t [sekunda]")
plt.ylabel("Sygnał")
plt.show()
plt.savefig("u")