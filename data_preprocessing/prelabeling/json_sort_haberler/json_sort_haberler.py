import json
import pandas as pd


def time_value(time):

    hours, minutes = time.split(":")

    hours = int(hours) * 60
    minutes = int(minutes)

    total_time = hours + minutes
    return total_time


def add_1day(a_date):

    day, month, year = a_date.split(".")

    day = int(day)
    month = int(month)
    year = int(year)

    day = day+1

    new_date = "{}.{}.{}".format(str(day), str(month), str(year))
    return new_date


def reformat_date(a_date):

    day, month, year = a_date.split(".")

    if len(day) < 2:
        day = day.zfill(2)
    if len(month) < 2:
        month = month.zfill(2)

    new_date = "{}.{}.{}".format(day, month, year)

    return new_date




NAME = "haberler"

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

for i in range(len(data)):

    for compare_key, compare_date in compare.items():
        if reformat_date(data[i]["Date"]) in compare_date:
            date = compare_key


    print(date)
    print(i)

    # finds if the date exists in the Excel sheet
    matching_row = df[df['Date'] == date]
    # print(matching_row)

    if len(matching_row) == 0:

        print(data[i]["Title"], " date doesnt exist")
        failed.append((data[i]["Date"] ,data[i]["Title"]))

    else:

        # gets if value on that date was negative or positive
        target = matching_row.iloc[0]["close-close[1]"]
        # print(target)

        if target < 0:
            neg.append(data[i])
        else:
            pos.append(data[i])


# for dictionary in negative list
for di in neg:

    filename = "{}_{}".format(NAME, di["Date"])
    file_path = "{}/{}{}".format(NEG_PATH, filename, ".txt")

    # write content as .txt into negative folder
    with open(file_path, "w") as f:
        f.write(di["Title"])

# for dictionary in positive list
for di in pos:

    filename = "{}_{}".format(NAME, di["Date"])
    file_path = "{}/{}{}".format(POS_PATH, filename, ".txt")

    # write content as .txt into positive folder
    with open(file_path, "w") as f:
        f.write(di["Title"])

# print(neg)
# print(pos)

# totals
print("positive: ", len(neg))
print("negative: ", len(pos))
print("failed: ", len(failed))

print("failed dictionaries: ", failed)

# adds failed dictionaries and associated unique values
with open("data/failed.txt", "a") as f:
    towrite = "{} {}{}".format(JSON_PATH, str(failed), "\n")
    f.write(towrite)
