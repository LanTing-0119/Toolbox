from pdf2docx import Converter
import mammoth
import os

# Define the file paths
pdf_file_path = "/Users/lanting/work/multifactor_prognosis/papers/ECG interpretation from pathophysiology to clinical applications.pdf"
word_file_path = pdf_file_path.replace(".pdf", ".docx")
html_file_path = pdf_file_path.replace(".pdf", ".html")

# Convert PDF to Word
cv = Converter(pdf_file_path)
cv.convert(word_file_path)
cv.close()

# Convert Word to HTML
with open(word_file_path, "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html_content = result.value

# Save the HTML file
with open(html_file_path, "w") as html_file:
    html_file.write(html_content)

html_file_path