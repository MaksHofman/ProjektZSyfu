"""
Lore
Ogulnie uzywamy CRC dla mnieszych paczek 8bitowych( i 8 bedzie takich paczek) dodajemy 7 bitow do kazdego modulo
wiec bedzie extra 56bitow wiec spoko i wykrywa jak jest nawet 8 bitow zle w 8 bitwej paczce.

stronka z wytlumaczniem co to crc - https://pl.wikipedia.org/wiki/Cykliczny_kod_nadmiarowy
"""
import random
def Rozdzielenie_64bitow_na_8paczek_8bitow(Calo_bitowa_wiadomosc):
    paczka_nr1 = []
    paczka_nr2 = []
    paczka_nr3 = []
    paczka_nr4 = []
    paczka_nr5 = []
    paczka_nr6 = []
    paczka_nr7 = []
    paczka_nr8 = []
    for _ in range(len(Calo_bitowa_wiadomosc)):
        if _ <= 7:
            paczka_nr1.append(Calo_bitowa_wiadomosc(_))
        elif _ <= 15 and _ > 7:
            paczka_nr2.append(Calo_bitowa_wiadomosc(_))
        elif _ <= 23 and _ > 15:
            paczka_nr3.append(Calo_bitowa_wiadomosc(_))
        elif _ <= 31 and _ > 23:
            paczka_nr4.append(Calo_bitowa_wiadomosc(_))
        elif _ <= 39 and _ > 31:
            paczka_nr5.append(Calo_bitowa_wiadomosc(_))
        elif _ <= 47 and _ > 39:
            paczka_nr6.append(Calo_bitowa_wiadomosc(_))
        elif _ <= 55 and _ > 47:
            paczka_nr7.append(Calo_bitowa_wiadomosc(_))
        elif _ <= 63 and _ > 55:
            paczka_nr8.append(Calo_bitowa_wiadomosc(_))

def Podanie_8_bitowego_Vektora_do_zaszyfrowania():
    Vetor_przyjety= []
    x = True
    z = 0
    while x:
        z += 1
        _ = input("podaj bit")
        if _.isspace():
            x = False
            break
        Vetor_przyjety.append(int(_))
        print(f"wpisano juz {z} bitow")
    print(Vetor_przyjety)
    return Vetor_przyjety

def xor(a, b):
    return a ^ b

"""
Baza tego to jest xor
"""
def crc_remainder(message, key):
    # Dopiszemy zero na końcu wiadomości
    message = message + [0] * (len(key) - 1)
    # Kopia wiadomości
    crc = message[:]
    # Długość klucza CRC
    key_length = len(key)

    # Pętla po każdym bicie wiadomości
    for i in range(len(message) - key_length + 1):
        # Jeśli aktualny bit jest równy 1, wykonujemy operację XOR z kluczem
        if crc[i] == 1:
            for j in range(key_length):
                crc[i + j] ^= key[j]

    # Usuwamy dodatkowe bity, które były dodane na końcu wiadomości
    return crc[-key_length + 1:]

def Filipownie_bitow(Vetor_przyjety, bit):
    if Vetor_przyjety[bit] == 1:
        Vetor_przyjety[bit] = 0
    elif Vetor_przyjety[bit] == 0:
        Vetor_przyjety[bit] = 1
def Wprowadznie_bledu_do_wiadomosci(Cala_wiadmosc, ilosc_beldow):
    for i in range(ilosc_beldow):
        Filipownie_bitow(Cala_wiadmosc, random.randint(0,14))
    return Cala_wiadmosc

def sprawdzanie_czy_jest_blad(wiadomosc, klucz):
    czesc_wiadomosci = []
    czesc_modulo = []
    for _ in range(len(wiadomosc)):
        if _ <= 7:
            czesc_wiadomosci.append(wiadomosc(_))
        elif _ > 7 and _ < 14:
            czesc_modulo.append(wiadomosc(_))
        else:
            raise ValueError("Zaduzo bitow")
    modulo_wiadmosci = crc_remainder(czesc_wiadomosci, klucz)
    if modulo_wiadmosci == czesc_modulo:
        return 0, czesc_wiadomosci
    else:
        return 1
def Sprawdzanie_i_wysyalknie_posby(wiadomosc, klucz):
    x, poprawna_wiadomosc = sprawdzanie_czy_jest_blad(wiadomosc, klucz)
    if x == 0:
        return poprawna_wiadomosc
    elif x == 1:
        pass #nw narazie jak to zorbic zeby poprosilo o ponowne wyslanie


def sklejanie_calej_wiadomosci(w1, w2, w3, w4, w5, w6, w7, w8):
    cala_wiadomosc = []
    cala_wiadomosc.extend(w1)
    cala_wiadomosc.extend(w2)
    cala_wiadomosc.extend(w3)
    cala_wiadomosc.extend(w4)
    cala_wiadomosc.extend(w5)
    cala_wiadomosc.extend(w6)
    cala_wiadomosc.extend(w7)
    cala_wiadomosc.extend(w8)
    return cala_wiadomosc

def Caly_Program(input):
    pass

if __name__ == "__main__":
    key = [1, 0, 0, 0, 0, 1, 1, 1]
    Vetor_przyjety = [1, 0, 1, 0, 0, 1, 1, 0]
    #Vetor_przyjety = Podanie_8_bitowego_Vektora_do_zaszyfrowania()
    ResztaCrc = crc_remainder(Vetor_przyjety, key)
    print("Zaszyfrowana wiadomość:", ResztaCrc)
    Vetor_przyjety.extend(ResztaCrc)
    print(Vetor_przyjety)
    Vetor_przyjety_kopia_na_puzniej = Vetor_przyjety.copy() # To jest jak juz wykryje blad zeby maszyna wyslal poprawny kod sprawdzarce
    zepsuta_wiadomosc = Wprowadznie_bledu_do_wiadomosci(Vetor_przyjety, 8)
    print(zepsuta_wiadomosc)