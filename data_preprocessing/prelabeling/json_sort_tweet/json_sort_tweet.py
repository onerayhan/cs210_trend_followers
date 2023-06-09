import json
import pandas as pd


NAME = "tweet"

JSON_PATH = "{}{}".format(NAME, ".json")
NEG_PATH  = "{}_{}".format("data/neg", NAME)
POS_PATH  = "{}_{}".format("data/pos", NAME)

with open("date_compare.json", "r") as fi:
    compare = json.load(fi)

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

# print(data)

neg = []
pos = []
failed = []
df = pd.read_excel("XU100.xlsx")

for i in data["date"].keys():

    i = int(i)

    for compare_key, compare_date in compare.items():
        if data["date"][str(i)] in compare_date:
            date = compare_key
            print(date)
            break


    matching_row = df[df['Date'] == date]
    # print(matching_row)


    if len(matching_row) == 0:

        print(data["text"][str(i)], " date doesnt exist")
        failed.append((data["date"][str(i)], data["text"][str(i)]))

    else:

        # gets if value on that date was negative or positive
        target = matching_row.iloc[0]["close-close[1]"]
        # print(target)

        if target < 0:
            neg.append({"date": data["date"][str(i)], "text": data["text"][str(i)], "time":data["time"][str(i)]})
        else:
            pos.append({"date": data["date"][str(i)], "text": data["text"][str(i)], "time":data["time"][str(i)]})


# for dictionary in negative list
id = 0
for di in neg:

    filename = "{}_{}_{}".format(NAME, di["date"], id)
    file_path = "{}/{}{}".format(NEG_PATH, filename, ".txt")

    print(filename)
    # write content as .txt into negative folder
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(di["text"])

    id = id+1

# for dictionary in positive list
for di in pos:

    filename = "{}_{}_{}".format(NAME, di["date"], id)
    file_path = "{}/{}{}".format(POS_PATH, filename, ".txt")

    # write content as .txt into positive folder
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(di["text"])

    id = id + 1

# print(neg)
# print(pos)

# totals
print("positive: ", len(neg))
print("negative: ", len(pos))
print("failed: ", len(failed))

print("failed dictionaries: ", failed)

# adds failed dictionaries and associated unique values
with open("data/failed.txt", "a", encoding="utf-8") as f:
    towrite = "{} {}{}".format(JSON_PATH, str(failed), "\n")
    f.write(towrite)