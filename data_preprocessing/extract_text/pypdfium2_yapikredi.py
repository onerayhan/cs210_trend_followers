# coding: utf8
import pypdfium2 as pdfium
import os
import string
import json


"""
    using pypdfium2 to get necessary text from gedik pdfs located in data/yapikredi_PDF
    put all extracted text into a list of dictionaries where date, count, paragraph are keys
    put the combined dictionaries into .json file
"""

PDF_LIST_PATH = "data/gedik_PDF"

# the list of dictionaries
pdfs = []

# store filenames of error-prone PDFs
broken_pdf = []

order = 1

for filename in os.listdir(PDF_LIST_PATH):

    pdf_dict = {}
    try:

        pdf = pdfium.PdfDocument("{}{}".format(PDF_LIST_PATH, filename))

    except pdfium._helpers.misc.PdfiumError:
        print("broken")
        broken_pdf.append(filename)

    page = pdf[1]  # which page
    textpage = page.get_textpage()

    text_all = textpage.get_text_range()

    # replacing characters that create unicode error
    text_all = text_all.replace("\u25cf", "###")
    text_all = text_all.replace('\ufffe', "-")

    text_all = text_all.replace("\r\n", " ")

    # getting text between two titles
    text_extract = text_all[text_all.find("Hisse Senedi: ") + len("Hisse Senedi: "): text_all.find("UsdTry EurTry")]

    # remove unnecessary punctuation in the beginning
    text1 = text_extract[:5]
    text2 = text_extract[5:]
    text1 = text1.translate(str.maketrans('', '', string.punctuation)).strip()

    text_final = text1 + text2
    # print(filename)

    # use filename components as keys
    yapikredi, date, count = filename[:-4].split("_")

    pdf_dict["date"] = date
    pdf_dict["count"] = count
    pdf_dict["paragraph"] = text_final
    print("dict created", order)
    pdfs.append(pdf_dict)
    order = order + 1

print(pdfs)

with open ("data/pdf_dicts.json", "a") as f:
    json.dump(pdfs, f)

print(broken_pdf)
