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



