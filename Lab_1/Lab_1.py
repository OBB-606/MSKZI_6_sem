text = "Александр_Шелудянкин_Валерий_Окунев_Данила_Журавлев_ИСБ-119_3"
text_list = []
for i in text:
    text_list.append(i)
n = int(len(text)**0.5) + 1
m = n
table = []
for i in range(n):
    table.append([0]*m)

for i in range(len(table)):
    for j in range(len(table[i])):
        try:
            table[i][j] = text_list.pop(0)
        except IndexError:
            table[i][j] = "*"
for i in range(len(table)):
    print(table[i])

coord_dict: dict = {}

for i in range(len(table)):
    for j in range(len(table[i])):
        coord_dict[table[i][j]] = [i, j]


def encrypted(text: str, coord_dict: dict, table: list):
    encrypted_text = ""
    for i in text:
        try:
            encrypted_text += table[coord_dict[i][1]][coord_dict[i][0]]
        except IndexError:
            pass
    return encrypted_text


encrypted_text = encrypted(text, coord_dict, table)


def decrypted(encrypted_text: str, coord_dict: dict, table: list):
    decrypted_text = ""
    for i in encrypted_text:
        decrypted_text += table[coord_dict[i][0]][coord_dict[i][1]]
    return decrypted_text


decrypted_text = decrypted(text, coord_dict, table)
print(encrypted_text)
print(decrypted_text)
print(f"{len(encrypted_text)}, {len(decrypted_text)}")

