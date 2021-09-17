somma = 0
with open("file.txt", "r") as txt_file:
    for line in txt_file:
        somma += float(line[104:109])

print(somma/64)