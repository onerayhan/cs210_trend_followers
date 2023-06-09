import pypdfium2 as pdfium
import os
import json


"""
    using pypdfium2 to get necessary text from akbank pdfs located in data/akbank_PDF
    put all extracted text into a list of dictionaries where date, monthAgo, count, paragraph are keys
    put the combined dictionaries into .json file
"""


PDF_LIST_PATH = "data/akbank_PDF"

# the list of dictionaries
pdfs = []

order = 1

for filename in os.listdir(PDF_LIST_PATH):

    pdf_dict = {}

    pdf = pdfium.PdfDocument("{}\\{}".format(PDF_LIST_PATH, filename))
    page = pdf[1]  # which page
    textpage = page.get_textpage()

    text_all = textpage.get_text_range()

    # replacing characters that create unicode error
    text_all = text_all.replace("\u25cf", "###")
    text_all = text_all.replace('\ufffe', "-")

    text_all = text_all.replace("\r\n", " ")

    # "###" characters signify articles, we want the text between
    text_final = text_all[text_all.find("###")+4: text_all.find("###", text_all.find("###")+1)]
    print(filename)

    # use filename components as keys
    akbank, date, monthsAgo, count = filename[:-4].split("_")

    pdf_dict["date"] = date
    pdf_dict["monthAgo"] = monthsAgo
    pdf_dict["count"] = count
    pdf_dict["paragraph"] = text_final.strip()

    print("dict created", order)
    pdfs.append(pdf_dict)
    order = order + 1

print(pdfs)

with open("data/pdf_dicts.json", "a") as f:
    json.dump(pdfs, f)
