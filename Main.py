"""
Lore
Ogulnie uzywamy CRC dla mnieszych paczek 8bitowych( i 8 bedzie takich paczek) dodajemy 7 bitow do kazdego modulo
wiec bedzie extra 56bitow wiec spoko i wykrywa jak jest nawet 8 bitow zle w 8 bitwej paczce.

stronka z wytlumaczniem co to crc - https://pl.wikipedia.org/wiki/Cykliczny_kod_nadmiarowy
"""
import random
array = list[int]
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
            paczka_nr1.append(Calo_bitowa_wiadomosc[_])
        elif _ <= 15 and _ > 7:
            paczka_nr2.append(Calo_bitowa_wiadomosc[_])
        elif _ <= 23 and _ > 15:
            paczka_nr3.append(Calo_bitowa_wiadomosc[_])
        elif _ <= 31 and _ > 23:
            paczka_nr4.append(Calo_bitowa_wiadomosc[_])
        elif _ <= 39 and _ > 31:
            paczka_nr5.append(Calo_bitowa_wiadomosc[_])
        elif _ <= 47 and _ > 39:
            paczka_nr6.append(Calo_bitowa_wiadomosc[_])
        elif _ <= 55 and _ > 47:
            paczka_nr7.append(Calo_bitowa_wiadomosc[_])
        elif _ <= 63 and _ > 55:
            paczka_nr8.append(Calo_bitowa_wiadomosc[_])
    return paczka_nr1, paczka_nr2, paczka_nr3, paczka_nr4, paczka_nr5, paczka_nr6, paczka_nr7, paczka_nr8

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

def Filipownie_bitow(Vetor_przyjety, bit: int):
    if Vetor_przyjety[bit] == 1:
        Vetor_przyjety[bit] = 0
    elif Vetor_przyjety[bit] == 0:
        Vetor_przyjety[bit] = 1

#zreworkowac trzeba to
def Wprowadznie_bledu_do_wiadomosci(Cala_wiadmosc,ilosc_beldow):
    for i in range(random.randint(0, ilosc_beldow)):
        Filipownie_bitow(Cala_wiadmosc, int(random.randint(0, 14)))
        ilosc_beldow -= 1
    return Cala_wiadmosc, ilosc_beldow

def sprawdzanie_czy_jest_blad(wiadomosc, klucz):
    czesc_wiadomosci = []
    czesc_modulo = []
    for _ in range(len(wiadomosc)):
        if _ <= 7:
            czesc_wiadomosci.append(wiadomosc[_])
        elif _ > 7 and _ <= 14:
            czesc_modulo.append(wiadomosc[_])
        else:
            raise ValueError("Zaduzo bitow")
    modulo_wiadmosci = crc_remainder(czesc_wiadomosci, klucz)
    if modulo_wiadmosci == czesc_modulo:
        return 0, czesc_wiadomosci
    else:
        return 1, czesc_wiadomosci
def Sprawdzanie_i_wysyalknie_posby(wiadomosc, klucz):
    x, poprawna_wiadomosc = sprawdzanie_czy_jest_blad(wiadomosc, klucz)
    if x == 0:
        return poprawna_wiadomosc
    elif x == 1:
        pass #nw narazie jak to zorbic zeby poprosilo o ponowne wyslanie


def pod_zes_paczka_handler(paczka,paczka_pre_zaszyfrowana, key, ilosc_bledow, output):
    back_up = paczka.copy()
    back_up.extend(paczka_pre_zaszyfrowana)
    paczka_zaszyfrowana_z_bledem, ilosc_bledow_updated = Wprowadznie_bledu_do_wiadomosci(back_up, ilosc_bledow)
    czy_jest_dobrze, poprawna_wiadomosc = sprawdzanie_czy_jest_blad(paczka_zaszyfrowana_z_bledem, key)

    if czy_jest_dobrze == 1:
        pod_zes_paczka_handler(paczka, paczka_pre_zaszyfrowana, key, ilosc_bledow_updated, output)
    elif czy_jest_dobrze == 0:
        output.append(poprawna_wiadomosc)
        return poprawna_wiadomosc
    else:
        raise Exception("pod_paczka_handler niepoprawnie dziala")
def paczka_handler(paczka, key, ilosc_bledow, output):
    paczka_pre_zaszyfrowana = crc_remainder(paczka, key)
    return pod_zes_paczka_handler(paczka, paczka_pre_zaszyfrowana, key, ilosc_bledow, output)

def Caly_Program(input: array) -> array:
    key = [1, 0, 0, 0, 0, 1, 1, 1]
    ilosc_bledow = 8
    p1, p2, p3, p4, p5, p6, p7, p8 = Rozdzielenie_64bitow_na_8paczek_8bitow(input)
    Paczka_array = [p1, p2, p3, p4, p5, p6, p7, p8]
    out_Paczki = []
    for x in range(len(Paczka_array)):
        _ = paczka_handler(Paczka_array[x], key, ilosc_bledow, out_Paczki)
    output = []
    for i in out_Paczki:
        output.extend(i)

    if output == input:
        print("udalo sie pomyslnie przeslac")
        print(f"input: {input}")
        print(f"output: {output}")
        return output
    else:
        raise ValueError("cos poszlo nie tak")

def random_64_bit_test_vector_generator():
    random_array = [random.randint(0, 1) for _ in range(64)]
    return random_array

if __name__ == "__main__":
    key = [1, 0, 0, 0, 0, 1, 1, 1]
    Testowy_vector = [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
    Caly_Program(Testowy_vector)