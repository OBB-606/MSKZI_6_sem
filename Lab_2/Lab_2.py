import random
import time


def get_random_digit():
    return random.randint(0, 255)


def generated_key_for_substitution(list_of_bytes: list):
    helper_list = []  # список с уникальными значениями байт из списка байтов файла
    final_list = []
    helper_set = set()
    for i in list_of_bytes:
        if i not in helper_list:
            helper_list.append(i)
    while len(helper_list) != len(helper_set):
        helper_set.add(random.randint(0, 255))
    for i in helper_set:
        final_list.append(i)
    random.shuffle(final_list)
    with open("keys/substitution_key.txt", "w") as write_file:
        for i in range(len(helper_list)):
            write_file.write(f"{str(helper_list[i])} ")
            write_file.write(f"{str(final_list[i])} ")


def get_input_file_binary_format(list_of_bytes: list):
    with open("input/input.txt", "w") as write_file:
        for i in list_of_bytes:
            write_file.write(f"{i} ")


def write_files_with_binary_mode(filename: str, list_of_bytes: list):
    with open(f"{filename}", "wb") as write_file:
        write_file.write(bytes(list_of_bytes))


def read_files_with_binary_mode(filename: str):
    with open(f"{filename}", "rb") as read_file:
        binary = read_file.read()
    return [i for i in binary]


def generated_key_for_permutation():
    size = random.randint(3, 100)
    key = [i for i in range(size)]
    random.shuffle(key)
    with open("keys/permutation_key.txt", "w") as write_file:
        for i in key:
            write_file.write(f"{i} ")


def generated_key_for_vigenere():
    size = random.randint(3, 100)
    key_list = [get_random_digit() for i in range(size)]
    with open("keys/vigenere_key.txt", "w") as write_file:
        for i in key_list:
            write_file.write(f"{i} ")


def generate_key_for_disposable_notepad(list_of_bytes: list):
    key = [get_random_digit() for i in list_of_bytes]
    with open("keys/disposable_notepad_key.txt", "w") as write_file:
        for i in key:
            write_file.write(f"{i} ")


def substitution(list_of_bytes: list, filename: str):  # подстановка
    # Ключ представляет из себя последовательность байт, где нечетные байты - уникальные значения байт из исходного
    # файла, а четные заменяющие байты. Создаем два словаря, в которых хранится ключ для шифрования и
    # расшифровывания. В первом из них ключ - значение байта исходного файла, значение - заменяющий байт Во втором
    # наоборот, он для расшифровки.
    #
    key_dict_1: dict = {}
    key_dict_2: dict = {}
    with open("keys/substitution_key.txt", "r") as read_file:  # открываем файл с сгенерированным ключом и помещаем
        # значение ключа в переменную
        tmp = read_file.read()  # str
    key = tmp.split()  # Создаем список и строки, с помощью split()
    for i in range(0, len(key) - 1, 2):  # пробегаемся по всей длине ключа и в двух словарях как было описано выше
        # сопоставляем значения друг другу
        key_dict_1[key[i]] = key[i + 1]
        key_dict_2[key[i + 1]] = key[i]
    # шифруем
    result_list = [int(key_dict_1[str(i)]) for i in list_of_bytes]
    # Бежим по списку и добавляем в финальный список байтов значения
    # словаря до данному ключу
    write_files_with_binary_mode(f"output/enc/{filename}", result_list)
    list_of_bytes.clear()
    result_list.clear()
    # дешифруем
    list_of_bytes = [int(i) for i in read_files_with_binary_mode(f"output/enc/{filename}")]
    result_list = [int(key_dict_2[str(i)]) for i in list_of_bytes]
    # при дешифровке list_of_bytes - список байтов зашифрованного файла
    # Бежим по списку и добавляем в финальный список байтов значения словаря до данному ключу
    write_files_with_binary_mode(f"output/dec/{filename}", result_list)


def permutation(list_of_bytes: list, filename: str):  # перестановка
    with open("keys/permutation_key.txt", "r") as read_file:
        tmp = read_file.read()
    key = tmp.split()
    list_enc = []
    tail = 0
    start = 0
    stop = len(key)
    step = 1
    if len(list_of_bytes) % len(key) == 0:
        while start < len(list_of_bytes):
            tmp = list_of_bytes[start:stop:step]
            for i in key:
                list_enc.append(tmp[int(i)])
            start += len(key)
            stop += len(key)
    else:
        while True:
            if len(list_of_bytes) % len(key) == 0:
                break
            else:
                list_of_bytes.append(random.randint(0, 255))
                tail += 1
        while start < len(list_of_bytes):
            tmp = list_of_bytes[start:stop:step]
            for i in key:
                list_enc.append(tmp[int(i)])
            start += len(key)
            stop += len(key)
    write_files_with_binary_mode(f"output/enc/{filename}", list_enc)
    list_enc = [int(i) for i in read_files_with_binary_mode(f"output/enc/{filename}")]

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

    for i in range(tail):
        list_dec.pop()
    write_files_with_binary_mode(f"output/dec/{filename}", list_dec)


def vigenere(list_of_bytes: list, filename: str):  # виженера
    # Шифровка
    result_list = []
    with open("keys/vigenere_key.txt", "r") as read_file:
        tmp = read_file.read()
    key_vigenere = tmp.split()
    i = 0
    while i < len(list_of_bytes):
        for j in range(len(key_vigenere)):
            try:
                result_list.append(int(key_vigenere[j]) ^ int(list_of_bytes[i]))
                i += 1
            except IndexError:
                break
    write_files_with_binary_mode(f"output/enc/{filename}", result_list)
    result_list.clear()
    # Дешифровка
    list_of_bytes_enc = [int(i) for i in read_files_with_binary_mode(f"output/enc/{filename}")]
    i = 0
    while i < len(list_of_bytes_enc):
        for j in range(len(key_vigenere)):
            try:
                result_list.append(int(key_vigenere[j]) ^ list_of_bytes_enc[i])
                i += 1
            except IndexError:
                break
    write_files_with_binary_mode(f"output/dec/{filename}", result_list)


def disposable_notepad(list_of_bytes: list, filename: str):  # одноразовый блокнот
    with open("keys/disposable_notepad_key.txt", "r") as read_file:
        tmp = read_file.read()
    key_notepad = tmp.split()
    result_list = [(list_of_bytes[i] ^ int(key_notepad[i])) for i in range(len(list_of_bytes))]
    write_files_with_binary_mode(f"output/enc/{filename}", result_list)
    result_list.clear()
    list_of_bytes_enc = [int(i) for i in read_files_with_binary_mode(f"output/enc/{filename}")]
    result_list = [(list_of_bytes_enc[i] ^ int(key_notepad[i])) for i in range(len(list_of_bytes_enc))]
    write_files_with_binary_mode(f"output/dec/{filename}", result_list)


def executor():
    question = int(input("what encryption method would you like to use?\n"
                         "1 - substitution, 2 - permutation, 3 - vigenere, 4 - disposable_notepad: "))
    if question == 1:
        filename = input("filename is: ")
        start = time.time()
        list_of_bytes = read_files_with_binary_mode(filename)
        generated_key_for_substitution(list_of_bytes)
        substitution(list_of_bytes, filename)
        print(f"time: {round(time.time() - start, 5)} seconds")

    elif question == 2:
        filename = input("filename is: ")
        start = time.time()
        list_of_bytes = read_files_with_binary_mode(filename)
        get_input_file_binary_format(list_of_bytes)
        generated_key_for_permutation()
        permutation(list_of_bytes, filename)
        print(f"time: {round(time.time() - start, 5)} seconds")

    elif question == 3:
        filename = input("filename is: ")
        start = time.time()
        list_of_bytes = read_files_with_binary_mode(filename)
        get_input_file_binary_format(list_of_bytes)
        generated_key_for_vigenere()
        vigenere(list_of_bytes, filename)
        print(f"time: {round(time.time() - start, 5)} seconds")

    elif question == 4:
        filename = input("filename is: ")
        start = time.time()
        list_of_bytes = read_files_with_binary_mode(filename)
        get_input_file_binary_format(list_of_bytes)
        generate_key_for_disposable_notepad(list_of_bytes)
        disposable_notepad(list_of_bytes, filename)
        lob_2 = read_files_with_binary_mode("output/enc/1.docx")
        print(f"{len(list_of_bytes)}, {len(lob_2)}")
        print(f"time: {round(time.time() - start, 5)} seconds")


executor()
