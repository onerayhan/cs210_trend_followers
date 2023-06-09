import requests


"""
    gets .txt file of links and downloads PDFs from it 
    saves them to /data/yapikredi_PDF, folders need to be created beforehand
"""


LINK_LIST_PATH = "data/link_list.txt"
PDF_LIST_PATH  = "data/yapikredi_PDF/"
FAIL_PATH      = "data/failed_links.txt"

with open(LINK_LIST_PATH, "r") as f:

    # separates the .txt to 2 lists for url and date

    list_content = f.readlines()
    list_content.pop(0)

    list_content = [x.split("\t") for x in list_content]

    url_list  = [x[1] for x in list_content]
    date_list = [x[2][:-1] for x in list_content]

    # print(page_list)
    # print(date_list)
    # print(url_list)


headers = requests.utils.default_headers()

headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

# id of file

count = 1

# download pdf and save to pdf_path
# if save fails write the filename to fail.txt at FAIL_PATH

for url, date in zip(url_list, date_list):

    response = requests.get(url, headers=headers)

    pdf_path = "{}yapikredi_{}_{}.pdf".format(PDF_LIST_PATH, date, count)
    try:
        with open(pdf_path, 'xb') as f:

            try:

                f.write(response.content)
                print(pdf_path)
            except:

                print("no download for ", pdf_path)
                with open(FAIL_PATH, 'a') as fail:
                    fail.write(pdf_path+"\n")
    except FileExistsError:
        print("same file")

    count = count+1

print("Done")
