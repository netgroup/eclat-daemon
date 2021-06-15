somma = 0
with open("file.txt", "r") as txt_file:
    for line in txt_file:
        somma += float(line[7:12])

print(somma/64)