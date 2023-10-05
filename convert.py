import sys
from PyPDF2 import PdfReader

print(sys.argv[1])
reader = PdfReader(sys.argv[1])
number_of_pages = len(reader.pages)
r = ""
for i in range(number_of_pages):
    page = reader.pages[i]
    r += page.extract_text()

with open(sys.argv[2], "w") as file:
   file.write(r)


