import numpy as np
import matplotlib.pyplot as plt
import math

#zad 1
x = [1, 1, 0, 1]

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
def zad1():
    #koder
    print (x)
    print("koder")
    a = HammingKoder(x)
    print(a)
    #dekoder bez zmian
    print("dekoder bez zmian")
    b, S = HammingDekoder(a)
    print(b)
    print(S)
    #ddekoder ze zmianą
    print("dekoder ze zmianą")
    a[4] = not a[4]
    b1, S1 = HammingDekoder(a)
    print(b1)
    print(S1)

#zad1()

# #zad2
#   Macierz = np.array([
#     [0, 0, 0, 1],
#     [0, 0, 1, 0],
#     [0, 0, 1, 1],
#     [0, 1, 0, 0],
#     [0, 1, 0, 1],
#     [0, 1, 1, 0],
#     [0, 1, 1, 1],
#     [1, 0, 0, 0],
#     [1, 0, 0, 1],
#     [1, 0, 1, 0],
#     [1, 0, 1, 1],
#     [1, 1, 0, 0],
#     [1, 1, 0, 1],
#     [1, 1, 1, 0],
#     [1, 1, 1, 1]
#   ])

def HammingKoder15(wejscie):
    wejscie =np.array()
    Ik = np.eye(11, int)
    P = np.array([
        [1, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [1, 1, 0, 1],
        [0, 0, 1, 1],
        [1, 0, 1, 1],
        [0, 1, 1, 1],
        [1, 1, 1, 1]
    ])
    G = np.hstack(P, Ik)
    c = wejscie*G
    return c

