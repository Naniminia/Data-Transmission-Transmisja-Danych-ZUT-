import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd

Tc = 3.0
fs = 10000
fi = 180
f = 1000
N = int(Tc * fs)

x = np.linspace(0, Tc, N)

def dft(x):
    N = len(x)
    n=np.arange(N)
    k = n.reshape((N,1))
    e = np.exp(-2j*np.pi*k*n/N)
    return np.dot(e, x)

#plt.plot(dft(np.sin(2*np.pi*f*x)))
#plt.show()

#zad 2
def M(x):
    M = np.sqrt((np.real(dft(x)))**2+(np.imag(x))**2)
    return M

def Mprim(x):
    M1 = 10*log10(M(x))
    return M1

fk = x*fs/N

#zmienić skalę
plt.plot(M(np.sin(2*np.pi*f*x)))
plt.show()
plt.savefig("widmo")