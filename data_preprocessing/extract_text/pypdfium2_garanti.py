# coding: utf8
import pypdfium2 as pdfium
import os
import json


"""
    using pypdfium2 to get necessary text from garanti pdfs located in data/garanti_PDF
    put all extracted text into a list of dictionaries where date, count, paragraph are keys
    put the combined dictionaries into .json file
"""

PDF_LIST_PATH = "data/garanti_PDF"

# the list of dictionaries
pdfs = []

# store filenames of error-prone PDFs
broken_pdf = []

order = 1

for filename in os.listdir(PDF_LIST_PATH):

    pdf_dict = {}

    try:
        pdf = pdfium.PdfDocument("{}\\{}".format(PDF_LIST_PATH, filename))

    except pdfium._helpers.misc.PdfiumError:
        print("broken")
        broken_pdf.append(filename)

    page = pdf[2]  # which page
    textpage = page.get_textpage()

    text_all = textpage.get_text_range()

    # replacing characters that create unicode error
    text_all = text_all.replace("\u25cf", "###")
    text_all = text_all.replace('\ufffe', "-")
    text_all = text_all.replace("\u20ba", "TL")

    text_all = text_all.replace("\r\n", " ")

    # getting text between two titles
    text_extract = text_all[text_all.find("BİST-100")+len("BİST-100"):text_all.find("VİOP")]

    # removing unnecessary "-"
    text1 = text_extract[:5]
    text2 = text_extract[5:]
    text1 = text1.replace("–", "").strip()
    text_final = text1 + text2

    # print(filename)
    # print(text_final)

    # use filename components as keys
    garanti, date, count = filename[:-4].split("_")

    pdf_dict["date"] = date
    pdf_dict["count"] = count
    pdf_dict["paragraph"] = text_final.strip()

    if pdf_dict["paragraph"] == "":
        broken_pdf.append(filename)

    pdfs.append(pdf_dict)
    order = order + 1
    print("dict created", order)

print(pdfs)

with open("data/pdf_dicts.json", "a") as f:
    json.dump(pdfs, f)

print(broken_pdf)

# removed garanti_28.11.2022_117 not günlük bülten
