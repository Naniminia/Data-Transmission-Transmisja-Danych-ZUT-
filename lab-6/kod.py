import numpy as np
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

zad1()

#zad2
Macierz = np.array([
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [1, 0, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 1],
        [1, 1, 1, 0],
        [1, 1, 1, 1]
    ])

bp = [1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1] #b początkowe
# b[0] = bp[0]
# b[1] = bp[1]
# b[2] = bp[3]
# b[3] = bp[7]
# b[4] = bp[2]
# b[5] = bp[5]
# b[6] = bp[6]
# b[7] = bp[7]
# b[8] = bp[8]
# b[9] = bp[9]
# b[10] = bp[10]
# b[11] = bp[11]
# b[12] = bp[12]
# b[13] = bp[13]
# b[14] = bp[14]

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

def HammingKoder1511(wejscie):

    Ik = np.eye(11, dtype = int)

    G = np.hstack((P, Ik))
    c = np.dot(wejscie, G)
    c = c%2
    return c

def HammingDekoder1511(wejscie1):
    Pt = np.transpose(P)
    Ink = np.eye(4, dtype = int)
    H = np.hstack((Ink, Pt))
    Ht = np.transpose(H)
    s = np.dot(wejscie1, Ht)
    s = s%2
    SumaKontrolna = ((s[0]* pow(2, 0)) + (s[1] * pow(2, 1)) + (s[2] * pow(2, 2)) + s[3]*pow(2,3))
    return s, SumaKontrolna

# z = HammingKoder1511(bp)
# print(z)
# a, suma = HammingDekoder1511(z)
# print(suma)
# print(a)
# print("ze zmianą")
# z[4] = not z[4]
# print(z)
# a1, suma1 = HammingDekoder1511(z)
# print(suma1)
# print(a1)
