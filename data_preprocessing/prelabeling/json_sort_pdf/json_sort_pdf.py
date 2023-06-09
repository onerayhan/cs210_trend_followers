import json
import pandas as pd

NAME = "yapikredi"

JSON_PATH = "{}_{}".format(NAME, "pdfdicts_temiz_json.json")
NEG_PATH  = "{}_{}".format("data/neg", NAME)
POS_PATH  = "{}_{}".format("data/pos", NAME)

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

# print(data)

neg = []
pos = []
failed = []
df = pd.read_excel("XU100.xlsx")

for i in range(len(data)):

    date = data[i]["date"]
    print(date)

    matching_row = df[df['Date'] == date]
    # print(matching_row)

    if len(matching_row) == 0:

        print(data[i]["count"], " date doesnt exist")
        failed.append(data[i]["count"])

    else:

        target = matching_row.iloc[0]["close-close[1]"]
        # print(target)

        if target < 0:
            neg.append(data[i])
        else:
            pos.append(data[i])


for di in neg:

    filename = "{}_{}_{}".format(NAME, di["date"], di["count"])
    file_path = "{}/{}{}".format(NEG_PATH, filename, ".txt")

    with open(file_path, "a") as f:
        f.write(di["paragraph"])


for di in pos:

    filename = "{}_{}_{}".format(NAME, di["date"], di["count"])
    file_path = "{}/{}{}".format(POS_PATH, filename, ".txt")

    with open(file_path, "a") as f:
        f.write(di["paragraph"])

# print(neg)
# print(pos)

print(len(neg))
print(len(pos))
print(len(failed))

print("failed dictionaries: ", failed)

with open("data/failed.txt", "a") as f:

    towrite = "{} {}{}".format(JSON_PATH, str(failed), "\n")
    f.write(towrite)
