merged_results = []

# Sonuçlarhaberler.txt dosyasındaki sonuçları okuma
with open("sonuçlarhaberler.txt", "r") as file:
    lines = file.readlines()
    for i in range(0, len(lines), 2):
        result = eval(lines[i])
        merged_results.append(result)

# Sonuçlarkurumlar.txt dosyasındaki sonuçları okuma
with open("sonuçlarkurumlar.txt", "r") as file:
    lines = file.readlines()
    for i in range(0, len(lines), 2):
        result = eval(lines[i])
        merged_results.append(result)

# Tüm sonuçları yazdırma
with open("tumsonuçlar.txt", "w") as file:
    for result in merged_results:
        file.write(str(result) + "\n")
        file.write("--------------------\n")

print("Sonuçlar başarıyla 'tumsonuçlar.txt' dosyasına birleştirildi.")
