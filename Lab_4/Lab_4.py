from collections import Counter
from prettytable import PrettyTable
from math import log2
import numpy as np
from zipfile import ZipFile
import time
from tqdm import tqdm

def read_file_with_binary_mode(filename: str):
    with open(f"{filename}", "rb") as read_file:
        return [i for i in read_file.read()]

def binary_view_mode(list_of_bytes: list):
    return [(bin(i).replace("0", "", 1)).replace("b", "", 1) for i in list_of_bytes]


def count_value_bits(list_ob_bits: list): # рассчитывает частоты появления единиц и нулей в потоке битов бинарного представления входного файла
    bits = "".join(list_ob_bits) # сплошная строка бит
    count_0 = 0
    count_1 = 0
    count_bits = len(bits)
    for i in bits:
        if i == "0":
            count_0 += 1
        else:
            count_1 += 1
    p_0 = count_0 / count_bits #частота нулей
    p_1 = count_1 / count_bits # частота единиц
    return (p_0, p_1)


def count_value_bytes(list_of_bytes):
    tmp = dict(Counter(list_of_bytes))
    dict_freq_temp: dict = {}
    for i in tqdm(tmp):
            dict_freq_temp[i] = tmp[i] / len(list_of_bytes)
    return dict(sorted(dict_freq_temp.items(), key = lambda x: x[0])) # сортировка по ключу


def entropy_of_bits_and_bytes(bits: tuple, bytes: dict):
    entropy_of_bits = -bits[0] * log2(bits[0]) - bits[1] * log2(bits[1])
    list_of_frequency_bytes = [bytes[i] for i in bytes]
    entropy_of_bytes = 0
    for i in list_of_frequency_bytes:
        entropy_of_bytes += i * log2(i)

    return (entropy_of_bits, -entropy_of_bytes)


def count_series(list_of_bits: str):
    list_of_counts_series_0 = []
    list_of_counts_series_1 = []
    max_len_series_list = []
    max_len = 0
    len_series_0 = "0"
    len_series_1 = "1"
    while True:
        if list_of_bits.count(len_series_0) or list_of_bits.count(len_series_1): #  Если существует такая серия в последовательности бит
            list_of_counts_series_0.append(list_of_bits.count(len_series_0))
            list_of_counts_series_1.append(list_of_bits.count(len_series_1))
            len_series_0 += "0"
            len_series_1 += "1"
        else:
            break
    for i in tqdm(range(len(list_of_counts_series_0))):
        if list_of_counts_series_0[i] > list_of_counts_series_1[i] and (list_of_counts_series_0[i] != 0 and list_of_counts_series_1[i] != 0):
            max_len_series_list.append(list_of_counts_series_0[i])
            max_len = i + 1 # так как нужен не индекс, а количество
        elif list_of_counts_series_0[i] <= list_of_counts_series_1[i] and (list_of_counts_series_0[i] != 0 and list_of_counts_series_1[i] != 0):
            max_len_series_list.append(list_of_counts_series_1[i])
            max_len = i + 1
    return (max_len, max_len_series_list)


def matrix_and_rang_test(list_of_bits_tmp: list):
    list_of_bits = [int(i) for i in list_of_bits_tmp]
    start = 0
    stop = 1024
    step = 1
    length = len(list_of_bits)
    count_dets_list = []
    while True:
        if length - stop < 1024:
            break
        else:
            # В список добавляются определители матриц 32х32, которые получаются путем конвертации среза списка в массив numpy
            count_dets_list.append(round(np.linalg.det(np.array(list_of_bits[start:stop:step]).reshape(32,32)), 3))
            start += 1024
            stop += 1024

    return count_dets_list


def zip_and_unzip(filename: str, archive_name: str):
    with ZipFile(f"{archive_name}", 'w') as zip_file:
        zip_file.write(f"{filename}")
    return read_file_with_binary_mode(f"{archive_name}")


def main():
    filename = input("write filename: ")
    # filename = "1.png"
    list_of_bytes = read_file_with_binary_mode(filename)
    list_of_bits = binary_view_mode(list_of_bytes)
    start = time.time()
    # Частотные тесты
    with open("results/frequency_tests", "w") as write_file:
        bits = count_value_bits(list_of_bits)
        bytes = count_value_bytes(list_of_bytes)
        write_file.write(f"Результаты тестов:\n\n\np0 = {bits[0]}, p1 = {bits[1]}\n")
        if bits[0] + bits[1] == 1:
            write_file.write(f"p0 + p1 = {bits[0] + bits[1]} - Выполняется\n")
        else:
            write_file.write(f"p0 + p1 = {bits[0] + bits[1]} - Не выполняется\n")
        if abs(bits[0] - bits[1]) <= 0.0333:
            write_file.write(f"Разница в частотах: {abs(bits[0] - bits[1])}, файл 'Хороший'\n+-+-+-+-+-++-+-+-+-+-++-+-+-+-+-++-+-+-+-+-++-+-+-+-+-++-+-+-+-+-+\n")
        else:
            write_file.write(f"Разница в частотах: {abs(bits[0] - bits[1])}, файл не 'Хороший'\n+-+-+-+-+-++-+-+-+-+-++-+-+-+-+-++-+-+-+-+-++-+-+-+-+-++-+-+-+-+-+\n")
        write_file.write(f"Частоты встречания значения байт в потоке байт входного файла: \n")
        table = PrettyTable()
        table.field_names = ['value_byte', 'frequency_byte']
        sum_bytes = 0
        for i in bytes:
            table.add_row([i, bytes[i]])
            sum_bytes += bytes[i]
        write_file.writelines(f"{table}\n")
        write_file.write(f"Сумма частот байтов: {round(sum_bytes, 3)}\n+-+-+-+-+-++-+-+-+-+-++-+-+-+-+-++-+-+-+-+-++-+-+-+-+-++-+-+-+-+-+\n")

    # Этнропийные тесты
    with open('results/entropy_tests', "w") as write_file:
        results = entropy_of_bits_and_bytes(bits, bytes)
        write_file.write(f"Энтропийные тесты:\n\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
        write_file.write(f"Энтропия бит: {results[0]}\nЭнтропия байт: {results[1]}\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")

    # Серийные тесты
    res = count_series("".join(list_of_bits))
    with open('results/series_tests', "w") as write_file:
        write_file.write(f"Результаты серийных тестов: \n\n\n")
        table.clear()
        table.field_names = ['length', 'count']
        j = 1
        formula = 0
        for i in tqdm(range(len(res[1]))):
            table.add_row([i, res[1][i]])
            # formula += j * res[1][i]
            j += 1
        write_file.write(f"Максимальная длина серии: {res[0]}\n\n"
                         f"{table}\n\n")
                         # f"sum i*ni = nbit = {formula == len(''.join(list_of_bits))}\n\n\n"
                         # f"nbit = {len(''.join(list_of_bits))}, formula = {formula}")


    # Матрично-ранговый тест
    res = matrix_and_rang_test(list_of_bits)
    with open('results/matrix_and_rang_tests', "w") as write_file:
        write_file.write("Матрично ранговый тест: \n\n")
        count_0 = 0
        for i in res:
            if i == 0:
                count_0 += 1
        write_file.write(f"Количество вырожденных матриц: {count_0}\n\n\n"
                         f"Количество невырожденных матриц: {len(res) - count_0}\n\n"
                         f"Всего матриц: {len(res)}\n\n")

    # Тест на сжимаемость
    res = zip_and_unzip(f"{filename}", f"{filename}_archive")
    with open("results/compress_tests", "w") as write_file:
        write_file.write(f'Результаты теста на сжатие:\n\n\n')
        write_file.write(f"Длина исходного файла: {len(list_of_bytes)}\n\n\nДлина сжатого файла: {len(res)}\n\n\nКоэффициент сжатия: {len(res)/len(list_of_bytes)}")
    print(f"time running program: {round(time.time() - start, 4)} seconds")
if __name__ == '__main__':
    main()