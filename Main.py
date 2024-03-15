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

def hamming_encode(data):
    # Calculate number of parity bits required
    r = 0
    while 2**r < len(data) + r + 1:
        r += 1

    # Initialize codeword with zeros
    codeword = [0] * (len(data) + r)

    # Fill in data bits into codeword
    j = 0
    for i in range(len(codeword)):
        if i + 1 not in [2**x for x in range(r)]:
            codeword[i] = data[j]
            j += 1

    # Calculate parity bits
    for i in range(r):
        parity_index = 2**i - 1
        parity = 0
        for j in range(parity_index, len(codeword), 2 * (parity_index + 1)):
            for k in range(parity_index + 1):
                if j + k < len(codeword):
                    parity ^= codeword[j + k]
        codeword[parity_index] = parity

    return codeword

def hamming_decode(codeword):
    # Find number of parity bits
    r = 0
    while 2**r < len(codeword):
        r += 1

    # Initialize syndrome
    syndrome = 0

    # Calculate syndrome
    for i in range(r):
        parity_index = 2**i - 1
        parity = 0
        for j in range(parity_index, len(codeword), 2 * (parity_index + 1)):
            for k in range(parity_index + 1):
                if j + k < len(codeword):
                    parity ^= codeword[j + k]
        syndrome += parity * 2**i

    # Correct error if found
    if syndrome != 0:
        if syndrome <= len(codeword):
            codeword[syndrome - 1] ^= 1

    # Determine if there are more than 1 errors
    syndrome = 0
    for i in range(r):
        parity_index = 2**i - 1
        parity = 0
        for j in range(parity_index, len(codeword), 2 * (parity_index + 1)):
            for k in range(parity_index + 1):
                if j + k < len(codeword):
                    parity ^= codeword[j + k]
        syndrome += parity * 2**i

    if syndrome != 0:
        return None  # More than 1 error detected

    # Extract data bits
    decoded_data = []
    j = 0
    for i in range(len(codeword)):
        if i + 1 not in [2**x for x in range(r)]:
            decoded_data.append(codeword[i])

    return decoded_data

def Filipownie_bitow(Vetor_przyjety, bit):
    if Vetor_przyjety[bit] == 1:
        Vetor_przyjety[bit] = 0
    elif Vetor_przyjety[bit] == 0:
        Vetor_przyjety[bit] = 1


def Wprowadznie_bledu_do_wiadomosci(Cala_wiadmosc):
    i = random.randint(0, 88)
    for j in range(8):
        Filipownie_bitow(Cala_wiadmosc, j+i)

#96 bitow trezba potasowac
#dziala
def tasowanie_bitow(array_paczek):
    przetasowane = [15]*96
    for i in range(len(array_paczek)):
        z = i
        for j in range(12):
            przetasowane[z] = array_paczek[i][j]
            z += 8

    return przetasowane

#wazne
def od_tasownie_bitow(array_paczek):
    od_tasownie_array = []
    for i in range(8):
        z = 0
        for j in range(12):
            od_tasownie_array.append(array_paczek[i + z])
            z += 8
    return od_tasownie_array

def main(input, print_out = False):
    back_up = input
    p1,p2,p3,p4,p5,p6,p7,p8 = Rozdzielenie_64bitow_na_8paczek_8bitow(input)
    array_paczek_pre_kodowanie = [p1,p2,p3,p4,p5,p6,p7,p8]
    array_zakodowane = []
    for x in array_paczek_pre_kodowanie:
        array_zakodowane.append(hamming_encode(x))
    array_przetasowanie = tasowanie_bitow(array_zakodowane)
    Wprowadznie_bledu_do_wiadomosci(array_przetasowanie)
    od_tasownie_array = od_tasownie_bitow(array_przetasowanie)
    array_output = []
    b1, b2, b3, b4, b5, b6, b7, b8 = [],[],[],[],[],[],[],[]
    b_array = [b1,b2,b3,b4,b5,b6,b7,b8]
    for ta in range(int(len(od_tasownie_array)/12)):
        for i in range(12):
            b_array[ta].append(od_tasownie_array[i])
    print(b_array)
    for z in b_array:
        array_output.extend(hamming_decode(z))
    output = []
    output.extend(array_output)
    if print_out and input == back_up and input == output:
        print("udalo sie")
        print(f"Input = {input}")
        print(f"Output = {output}")
    elif print_out == False and input == back_up and input == output:
        return output
    else:
        print(f"Input = {input}")
        print(f"Output = {output}")
        raise ValueError("essa")


def random_64_bit_test_vector_generator():
    random_array = [random.randint(0, 1) for _ in range(64)]
    return random_array

if __name__ == "__main__":

    main(random_64_bit_test_vector_generator(), True)
    
    """wynik = 0
    probka = 100000

    for x in range(probka):
        try:
            main(random_64_bit_test_vector_generator())
            wynik += 1
        except ValueError:
            pass

    print(f"W {wynik}/{probka} przypadkach bylo dobrze")
    print(f"w {(wynik/probka)*100}% jest dobrze")
"""