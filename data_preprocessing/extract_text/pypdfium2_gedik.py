
import pypdfium2 as pdfium
import os
import json


"""
    using pypdfium2 to get necessary text from gedik pdfs located in data/gedik_PDF
    put all extracted text into a list of dictionaries where date, monthAgo, count, paragraph are keys
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

    pdf = pdfium.PdfDocument("{}\\{}".format(PDF_LIST_PATH, filename))
    page = pdf[0] # which page
    textpage = page.get_textpage()

    text_all = textpage.get_text_range()

    # replacing characters that create unicode error
    text_all = text_all.replace("\u25cf", "###")
    text_all = text_all.replace('\ufffe', "-")

    text_all = text_all.replace("\r\n", " ")

    # getting text between two titles
    text_final = text_all[text_all.find("BIST-100 Strateji")+len("BIST-100 Strateji"): text_all.find('Önemli Sektör Şirket Haberleri')]
    print(filename)

    # use filename components as keys
    gedik, date, monthsAgo, count = filename[:-4].split("_")

    pdf_dict["date"] = date
    pdf_dict["monthAgo"] = monthsAgo
    pdf_dict["count"] = count
    pdf_dict["paragraph"] = text_final.strip()

    print("dict created", order)
    pdfs.append(pdf_dict)
    order = order + 1

print(pdfs)

with open ("data/pdf_dicts.json", "a") as f:
    json.dump(pdfs, f)