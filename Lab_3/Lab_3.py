"""
Многораундовое шифрование. Порядок: Подстановка - гаммирование - перестановка - гаммирование - подстановка и тд
Исходный файл - поток байт.
Поток байт делится на блоки длинной 16 (желательно)
К каждому блоку по очереди применяются 3 криптографических примитива 16 раз с указанным в указанном выше порядке.
После применения 16 раз криптопримитивов уже зашифрованный блок записывается в бинарном режиме в файл.

"""
import random
import json
import time

def get_random_digit():
    return random.randint(0, 255)

def write_files_with_binary_mode(filename: str, list_of_bytes: list):
    with open(f"{filename}", "wb") as write_file:
        write_file.write(bytes(list_of_bytes))


def read_files_with_binary_mode(filename: str):
    with open(f"{filename}", "rb") as read_file:
        binary = read_file.read()
    return [i for i in binary]

def generate_key_for_permutation(length_list: int):
    key = [i for i in range(length_list)]
    random.shuffle(key)
    with open('keys/permutation_key.txt', 'w') as write_file:
        for i in key:
            write_file.write(f"{i} ")

def generate_key_for_substitution(list_of_bytes: list):
    helper_list = []
    helper_set = set()
    for i in list_of_bytes:
        if i not in helper_list:
            helper_list.append(i)
    while len(helper_list) != len(helper_set):
        helper_set.add(random.randint(0, 255))
    final_list = [i for i in helper_set]
    random.shuffle(final_list)
    with open("keys/substitution_key.txt", "w") as write_file:
        for i in range(len(helper_list)):
            write_file.write(f"{str(helper_list[i])} ")
            write_file.write(f"{str(final_list[i])} ")
    key_dict_1: dict = {}
    key_dict_2: dict = {}
    with open("keys/substitution_key.txt", "r") as read_file:
        tmp = read_file.read()
    key = tmp.split()
    for i in range(0, len(key) - 1, 2):
        key_dict_1[key[i]] = key[i + 1]
        key_dict_2[key[i + 1]] = key[i]
    with open('keys/key_dict_1.json', 'w') as json_write_file:
        json.dump(key_dict_1, json_write_file, indent=3)
    with open('keys/key_dict_2.json', 'w') as json_write_file:
        json.dump(key_dict_2, json_write_file, indent=3)

def generate_key_for_gamming(list_of_bytes: list):
    key = [get_random_digit() for i in list_of_bytes]
    with open("keys/gamming_key.txt", "w") as write_file:
        for i in key:
            write_file.write(f"{i} ")

def permutation_enc(list_of_bytes: list):
    with open("keys/permutation_key.txt", "r") as read_file:
        tmp = read_file.read()
    key = tmp.split()
    list_enc = []
    start = 0
    stop = len(key)
    step = 1
    while start < len(list_of_bytes):
        tmp = list_of_bytes[start:stop:step]
        for i in key:
            list_enc.append(tmp[int(i)])
        start += len(key)
        stop += len(key)
    return list_enc

def substitution_enc(list_of_bytes: list):
    with open('keys/key_dict_1.json', "r") as json_read_file:
        key_dict_1 = json.load(json_read_file)
    result_list = [int(key_dict_1[str(i)]) for i in list_of_bytes]
    return result_list

def gamming_enc(list_of_bytes: list):
    with open ("keys/gamming_key.txt", "r") as read_file:
        tmp = read_file.read()
    key_gamming = tmp.split()
    result_list = [(list_of_bytes[i] ^ int(key_gamming[i])) for i in range(len(list_of_bytes))]
    return result_list

def substitution_dec(list_of_bytes: list):
    with open("keys/key_dict_2.json", "r") as json_read_file:
        key_dict_2 = json.load(json_read_file)
    result_list = [int(key_dict_2[str(i)]) for i in list_of_bytes]
    return result_list

def permutation_dec(list_enc: list):
    with open("keys/permutation_key.txt", "r") as read_files:
        tmp = read_files.read()
    key = tmp.split()
    list_dec = []
    start = 0
    stop = len(key)
    step = 1
    while start < len(list_enc):
        tmp = list_enc[start:stop:step]
        for i in range(len(key)):
            list_dec.append(tmp[key.index(str(i))])
        start += len(key)
        stop += len(key)
    return list_dec

def gamming_dec(list_of_bytes: list):
    with open ("keys/gamming_key.txt", "r") as read_file:
        tmp = read_file.read()
    key_gamming = tmp.split()
    result_list = [(list_of_bytes[i] ^ int(key_gamming[i])) for i in range(len(list_of_bytes))]
    return result_list


def executor():
    filename  = input("write filename for cryptography action: ")
    list_of_bytes_temp = read_files_with_binary_mode(filename)
    list_of_bytes = []
    length_block_data = 16
    start = 0
    stop = length_block_data
    step  = 1
    while True:
        list_of_bytes.append(list_of_bytes_temp[start:stop:step])
        if stop > len(list_of_bytes_temp):
            break
        if len(list_of_bytes_temp) - stop < length_block_data and len(list_of_bytes_temp) - stop > 0:
            stop = len(list_of_bytes_temp)
        start += length_block_data
        stop += length_block_data

    tail = 0
    while len(list_of_bytes[-1]) != length_block_data: # Если длина последнего блока данных не равна выбранному блоку, то будет приписан "Хвост"
        list_of_bytes[-1].append(0)
        tail += 1

    generate_key_for_substitution(list_of_bytes_temp)
    generate_key_for_permutation(length_block_data)
    generate_key_for_gamming(list_of_bytes[0])
    # шифрование
    count = 0
    list_of_bytes_enc_temp = []
    start_enc = time.time()
    for block in list_of_bytes:
        tmp_lst = [block]
        for i in range(4):
            tmp_lst.append(gamming_enc(permutation_enc(gamming_enc(substitution_enc(tmp_lst.pop())))))
        count += 1
        for i in tmp_lst.pop():
            list_of_bytes_enc_temp.append(i)
    stop_enc = time.time() - start_enc
    print(f"time encryption: {stop_enc}")
    write_files_with_binary_mode(f'enc/{filename}', list_of_bytes_enc_temp)

    list_of_bytes_enc = []
    start = 0
    stop = length_block_data
    step = 1
    while True:
        list_of_bytes_enc.append(list_of_bytes_enc_temp[start:stop:step])
        if stop > len(list_of_bytes_enc_temp):
            break
        start += length_block_data
        stop += length_block_data

    # дешифрование
    list_of_bytes_dec = []
    start_dec = time.time()
    for block in list_of_bytes_enc:
        tmp_lst = [block]
        for i in range(4):
            tmp_lst.append(substitution_dec(gamming_dec(permutation_dec(gamming_dec(tmp_lst.pop())))))
        count += 1
        for i in tmp_lst.pop():
            list_of_bytes_dec.append(i)
    stop_dec = time.time() - start_dec
    for i in range(tail):
        list_of_bytes_dec.pop()
    write_files_with_binary_mode(f"dec/{filename}", list_of_bytes_dec)
    print(f"time decryption: {stop_dec}")

executor()
