import matplotlib.pyplot as plt
import math
import numpy as np

string1 = 'ABC'

def zamiana(string1):
    string3 = ''
    for i in string1:
        #string3 += bin(ord(i))[2:]
        string3 += bin(ord(i))[2:].zfill(8) #opcja z zapełnienem do 8 bitów
    return string3

print("Wartość: ", zamiana(string1)) #sprawdzenie funckji

string2 = zamiana(string1)
Tb = 1
W = 2
fn = W * pow(Tb, -1)
Tc = Tb * len(string2)
fs = 200
fi = 180
f = 1000
fn1 = (W + 1) / Tb
fn2 = (W + 2) / Tb

M = int(Tb*fs) #ilość próek fs przypadających na bit
N = len(string2)*M #obliczanie długości sygnał na podstawie bitów wejśćiowych

def modulacjaASK():
    # def kluczowanieASK(string2, fs, fn, Tb):
    #     A1 = 0
    #     A2 = 1
    #     wyjscie1 = []
    #     wyjscie2 = []
    #
    #     for n in range(0, N):
    #         t = n / fs
    #         wyjscie1.append(t)
    #         indeks = int(t / Tb)
    #         if string2[indeks] == '0':
    #             wyjscie2.append(A1 * (math.sin(2 * math.pi * fn * t)))
    #         else:
    #             wyjscie2.append(A2 * (math.sin(2 * math.pi * fn * t)))
    #     return wyjscie1, wyjscie2

    def KluczowanieASK(string2, A1, A2, fn, fs, Tb):
        wyjscie1 = []
        wyjscie2 = []
        for n in range(0, N):
            t = n / fs
            indeks = int(t / Tb)
            wyjscie1.append(t)

            if string2[indeks] == '0':
                wyjscie2.append(A1 * (math.sin(2 * math.pi * fn * t)))
            else:
                wyjscie2.append(A2 * (math.sin(2 * math.pi * fn * t)))
        return wyjscie1, wyjscie2
    A1 =1
    A2 = 2
    x, y = KluczowanieASK(string2, A1, A2, fn, fs, Tb)
    #x, y = KluczowanieASK(string2, A1=1, A2=2, fn, fs, Tb)
    plt.plot(x, y, label = "Sygnal ASK", color='magenta')
    plt.title('Sygnał ASK')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.savefig('ask_z.png')
    plt.show()

    #ASK po pomnożeniu przez sunusa
    def ASK_xt(y_ASK, fn, fs):
        wyjscie = []
        A = 1
        for n in range(len(y_ASK)):
            t = n / fs
            wyjscie.append(y[n] * (A * np.sin(2 * np.pi * fn * t)))
        return wyjscie

    wartosci_XT = ASK_xt(y, fn, fs)
    plt.plot(x, wartosci_XT, label = "Probki z ASK_xt")
    plt.title('Probki z ASK_xt (pomnozone przez sinusa') #ASK*sinus
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.savefig('ask_x.png')
    plt.show()

    def ASK_pt(wartosci_XT, M, fs):
        dt = 1 / fs
        calka = []
        for i in range(0, len(wartosci_XT), M):
            calka_bit = []
            suma = 0
            for j in range(M):
                if i + j < len(wartosci_XT):
                    suma += wartosci_XT[i + j] * dt
                    calka_bit.append(suma)
            calka.extend(calka_bit)
        return calka

    wartosci_pt = ASK_pt(wartosci_XT, M, fs)
    plt.plot(wartosci_pt, label='Całki wartość po pt', color='orange')
    plt.title('Całki wartość po pt (wszystkie próbki)')
    plt.xlabel('Numer próbki')
    plt.ylabel('Wartość całki')
    plt.legend()
    plt.savefig("ask_p.png")
    plt.show()
    def prog_h(x, M, margin=0.05):
        wartosc = x[M-1] #wartość na końcu pierwzsego bitu
        return wartosc - 0.001

    wartosc_progu = prog_h(wartosci_pt, M)

    #po progu, czuli c(t)
    def ASK_ct(wartosci_pt, wartosc_progu):
        wyjscie = []
        for value in wartosci_pt:
            if value >= wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = ASK_ct(wartosci_pt, wartosc_progu)
    plt.step(range(len(wartosci_ct)), wartosci_ct, label='ASK po progu', color='green')
    plt.title('ASK po progu')
    plt.xlabel('Numer próbki')
    plt.ylabel('Wartość')
    #plt.ylim(-0.1, 1.1) #lepiej widczone
    plt.legend()
    plt.savefig("ask_c.png")
    plt.show()

    for i in range(1, len(wartosci_ct) // M): #pomoc z interneru, nie byłam pewna jak zrobić
        plt.axvline(x=i*M, color='red', linestyle='--')

    def odczytywanie_bitow_ct(wartosci_ct, M, h):
        bity = []
        for i in range(0, len(wartosci_ct), M):
            wartosci1 = 0
            wartosci = 0
            for j in wartosci_ct[i:i + M]:
                if j == 1:
                    wartosci1 += 1
                elif j == 0:
                    wartosci += 1
                else:
                    print("blad :(")

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane=odczytywanie_bitow_ct(wartosci_ct, M, wartosc_progu)
    print("odczytane bity", odczytane)

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.step(range(len(string2)), [int(bit) for bit in string2], label='Początkowe bity', color='magenta')
    plt.title('Początkowe bity')
    plt.xlabel('Numer bitu')
    plt.ylabel('Wartość')
    plt.ylim(-0.1, 1.1)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.step(range(len(odczytane)), odczytane, label='Odczytane bity', color='orange')
    plt.title('Odczytane bity ASK')
    plt.xlabel('Numer bitu')
    plt.ylabel('Wartość')
    plt.ylim(-0.1, 1.1)
    plt.legend()

    plt.tight_layout()
    plt.savefig("porownanie_ASK.png")
    plt.show()

def modulacjaPSK():
    def KluczowaniePSK(string2, A1, A2, fn, fs, Tb):
        wyjsciePSK1 = []
        wyjsciePSK2 = []
        for n in range(0, N):
            t = n / fs
            indeks = int(t / Tb)
            wyjsciePSK1.append(t)

            if string2[indeks] == '0':
                wyjsciePSK2.append(math.sin(2 * math.pi * fn * t))
            else:
                wyjsciePSK2.append(math.sin(2 * math.pi * fn * t + math.pi))
        return wyjsciePSK1, wyjsciePSK2

    A1 =1
    A2 = 2
    x_PSK, y_PSK = KluczowaniePSK(string2, A1, A2, fn, fs, Tb)

    plt.plot(x_PSK, y_PSK, label = "Sygnal PSK", color='magenta')
    plt.title('Sygnał PSK')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.savefig('psk_z.png')
    plt.show()


    def PSK_xt(y_PSK, fn, fs):
        wyjscie = []
        for n in range(len(y_PSK)):
            t = n / fs
            wyjscie.append(y_PSK[n] * (np.sin(2 * np.pi * fn * t)))
        return wyjscie

    wartosci_XT = PSK_xt(y_PSK, fn, fs)
    plt.plot(wartosci_XT, label = "Probki z PSK_xt")
    plt.title('Probki z PSK_xt (pomnozone przez sinusa') #ASK*sinus
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.savefig('psk_x.png')
    plt.show()

    def PSK_pt(wartosci_XT, M, fs):
        dt = 1 / fs
        calka = []
        for i in range(0, len(wartosci_XT), M):
            calka_bit = []
            suma = 0
            for j in range(M):
                if i + j < len(wartosci_XT):
                    suma += wartosci_XT[i + j] * dt
                    calka_bit.append(suma)
            calka.extend(calka_bit)
        return calka

    wartosci_pt = PSK_pt(wartosci_XT, M, fs)
    plt.plot(wartosci_pt, label='Całki wartość po pt', color='orange')
    plt.title('Całki wartość po pt (wszystkie próbki)')
    plt.xlabel('Numer próbki')
    plt.ylabel('Wartość całki')
    plt.legend()
    plt.savefig("psk_p.png")
    plt.show()

    wartosc_progu = 0.01
    def PSK_ct(wartosci_pt, wartosc_progu):
        wyjscie = []
        for value in wartosci_pt:
            if value < wartosc_progu:
                wartosc1 = 1
                wyjscie.append(wartosc1)
            else:
                wartosc = 0
                wyjscie.append(wartosc)
        return wyjscie

    wartosci_ct = PSK_ct(wartosci_pt, wartosc_progu)
    plt.step(range(len(wartosci_ct)), wartosci_ct, label='PSK po progu', color='green')
    plt.title('PSK po progu')
    plt.xlabel('Numer próbki')
    plt.ylabel('Wartość')
    #plt.ylim(-0.1, 1.1) #lepiej widczone
    plt.legend()
    plt.savefig("psk_c.png")
    plt.show()

    for i in range(1, len(wartosci_ct) // M): #pomoc z interneru, nie byłam pewna jak zrobić
        plt.axvline(x=i*M, color='red', linestyle='--')

    def odczytywanie_bitow_ct(wartosci_ct, M, h):
        bity = []
        for i in range(0, len(wartosci_ct), M):
            wartosci1 = 0
            wartosci = 0
            for j in wartosci_ct[i:i + M]:
                if j == 1:
                    wartosci1 += 1
                elif j == 0:
                    wartosci += 1
                else:
                    print("blad :(")

            if wartosci1 > wartosci:
                bity.append(1)
            else:
                bity.append(0)
        return bity

    odczytane=odczytywanie_bitow_ct(wartosci_ct, M, wartosc_progu)
    print("odczytane bity", odczytane)

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.step(range(len(string2)), [int(bit) for bit in string2], label='Początkowe bity', color='magenta')
    plt.title('Początkowe bity')
    plt.xlabel('Numer bitu')
    plt.ylabel('Wartość')
    plt.ylim(-0.1, 1.1)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.step(range(len(odczytane)), odczytane, label='Odczytane bity', color='orange')
    plt.title('Odczytane bity PSK')
    plt.xlabel('Numer bitu')
    plt.ylabel('Wartość')
    plt.ylim(-0.1, 1.1)
    plt.legend()

    plt.tight_layout()
    plt.savefig("porownanie_PSK.png")
    plt.show()

def modulacjaFSK():
  A1 = 1
  A2 = 2
  def KluczowanieFSK(string2, A1, A2, fn1, fn2, fs, Tb):
    wyjscieFSK1 = []
    wyjscieFSK2 = []

    for n in range(0, N):
        t = n / fs
        indeks = int(t / Tb)
        wyjscieFSK1.append(t)
        if string2[indeks] == '0':
            wyjscieFSK2.append(A1 * np.sin(2 * np.pi * fn1 * t))
        else:
            wyjscieFSK2.append(A2 * np.sin(2 * np.pi * fn2 * t))  # Dodanie zer, gdy indeks jest poza zakresem lub bit to '1'
    return wyjscieFSK1, wyjscieFSK2

  x_FSK, y_FSK = KluczowanieFSK(string2, A1, A2, fn1, fn2, fs, Tb)
  plt.plot(x_FSK, y_FSK, label='Sygnał FSK')
  plt.title('Sygnał FSK')
  plt.xlabel('Czas [s]')
  plt.ylabel('Amplituda')
  plt.legend()
  plt.savefig("fsk_z.png")

  def FSK_x1_t(y_FSK, fn1, fs):
      wyjscie = []
      for n in range(len(y_FSK)):
          t = n / fs
          wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn1 * t)))
      return wyjscie

  fsk_t_x1 = FSK_x1_t(y_FSK, fn1, fs)
  plt.plot(x_FSK, fsk_t_x1, label='FSK dla fn1')
  plt.title('Sygnał FSK dla fn1')
  plt.xlabel('Czas [s]')
  plt.ylabel('Amplituda')
  plt.legend()
  plt.savefig("fsk_x1.png")
  plt.show()

  def FSK_x2_t(y_FSK, fn2, fs):
      wyjscie = []
      for n in range(len(y_FSK)):
          t = n / fs
          wyjscie.append(y_FSK[n] * (np.sin(2 * np.pi * fn2 * t)))
      return wyjscie

  fsk_t_x2 = FSK_x2_t(y_FSK, fn2, fs)
  plt.plot(x_FSK, fsk_t_x2, label='FSK dla fn2')
  plt.title('Sygnał FSK dla fn2')
  plt.xlabel('Czas [s]')
  plt.ylabel('Amplituda')
  plt.legend()
  plt.savefig("fsk_x2.png")
  plt.show()

  def FSK_p1_t(fsk_t_x1, M, fs):
      calki = []
      dt = 1 / fs
      for i in range(0, len(fsk_t_x1), M):
          calka_bit = []
          suma = 0
          for j in range(M):
              if i + j < len(fsk_t_x1):
                  suma += fsk_t_x1[i + j] * dt
                  calka_bit.append(suma)
          calki.extend(calka_bit)
      return calki

  fp1_calki = FSK_p1_t(fsk_t_x1, M, fs)
  plt.plot(fp1_calki, label='FSK po całce dla fn1', color='green')
  plt.title('FSK po całce dla fn1')
  plt.xlabel('Numer próbki')
  plt.ylabel('Wartość całki')
  plt.legend()
  plt.savefig("fsk_p1.png")
  plt.show()

  def FSK_p2_t(fsk_t_x2, M, fs):
      calki = []
      dt = 1 / fs
      for i in range(0, len(fsk_t_x2), M):
          calka_bit = []
          suma = 0
          for j in range(M):
              if i + j < len(fsk_t_x2):
                  suma += fsk_t_x2[i + j] * dt
                  calka_bit.append(suma)
          calki.extend(calka_bit)
      return calki
  fp2_calki = FSK_p2_t(fsk_t_x2, M, fs)
  plt.plot(fp2_calki, label='FSK po całce dla fn2', color='green')
  plt.title('FSK po całce dla fn2')
  plt.xlabel('Numer próbki')
  plt.ylabel('Wartość całki')
  plt.legend()
  plt.savefig("fsk_p2.png")
  plt.show()

  def FSK_p_t(fp1_calki, fp2_calki):
      wynik = []
      if len(fp1_calki) != len(fp2_calki):
          raise ValueError("Długości sygnałów nie są równe")
      else:
        for i in range(len(fp1_calki)):
          wynik.append(fp1_calki[i] - fp2_calki[i])
      return wynik

  FSK_pt = FSK_p_t(fp1_calki, fp2_calki)
  plt.plot(FSK_pt, label='FSK po całce dla różnicy fn1 i fn2', color='purple')
  plt.title('FSK po całce dla różnicy fn1 i fn2')
  plt.xlabel('Numer próbki')
  plt.ylabel('Wartość całki')
  plt.legend()
  plt.savefig("fsk_p.png")

  wartosc_progu = 0.01
  def FSK_ct(FSK_pt, wartosc_progu):
      wyjscie = []
      for value in FSK_pt:
          if value > wartosc_progu:
              wartosc1 = 1
              wyjscie.append(wartosc1)
          else:
              wartosc = 0
              wyjscie.append(wartosc)
      return wyjscie

  wartosci_ct = FSK_ct(FSK_pt, wartosc_progu)
  plt.step(range(len(wartosci_ct)), wartosci_ct, label='FSK po progu', color='green')
  plt.title('FSK po progu')
  plt.xlabel('Numer próbki')
  plt.ylabel('Wartość')
  # plt.ylim(-0.1, 1.1) #lepiej widczone
  plt.legend()
  plt.savefig("fsk_c.png")
  plt.show()

  def odczytywanie_bitow_ct(wartosci_ct, M, h):
      bity = []
      for i in range(0, len(wartosci_ct), M):
          wartosci1 = 0
          wartosci = 0
          for j in wartosci_ct[i:i + M]:
              if j == 1:
                  wartosci1 += 1
              elif j == 0:
                  wartosci += 1
              else:
                  print("blad :(")

          if wartosci1 > wartosci:
              bity.append(1)
          else:
              bity.append(0)
      return bity

  odczytane=odczytywanie_bitow_ct(wartosci_ct, M, wartosc_progu)
  print("odczytane bity", odczytane)

  plt.figure(figsize=(12, 6))

  plt.subplot(2, 1, 1)
  plt.step(range(len(string2)), [int(bit) for bit in string2], label='Początkowe bity', color='magenta')
  plt.title('Początkowe bity')
  plt.xlabel('Numer bitu')
  plt.ylabel('Wartość')
  plt.ylim(-0.1, 1.1)
  plt.legend()

  plt.subplot(2, 1, 2)
  plt.step(range(len(odczytane)), odczytane, label='Odczytane bity', color='orange')
  plt.title('Odczytane bity FSK')
  plt.xlabel('Numer bitu')
  plt.ylabel('Wartość')
  plt.ylim(-0.1, 1.1)
  plt.legend()

  plt.tight_layout()
  plt.savefig("porownanie_FSK.png")
  plt.show()

#modulacjaASK()
#modulacjaPSK()
modulacjaFSK()
