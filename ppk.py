import os
import csv
import re
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Directory containing all PDF files
pdf_folder = r"C:\Users\naqib\OneDrive\Documents\[APPS]\Python\ppk-report\PPK-NAQIB"
output_csv = "General_PPK_Report.csv"

# Prepare header for CSV
data_rows = [("Company Name", "Start Date", "End Date")]

# OCR Fallback Function
def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang='eng')
    return text

# Try extracting text normally, else use OCR
def get_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            text += extracted if extracted else ""
        if not text.strip():
            raise ValueError("No extractable text found.")
        return text
    except:
        return extract_text_with_ocr(pdf_path)

# Loop through all PDF files in folder
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        path = os.path.join(pdf_folder, filename)
        text = get_text_from_pdf(path)

        # Extract fields
        company = re.search(r"Nama Kontraktor\s*:\s*(.+)", text)
        start = re.search(r"Tarikh Mula Berkuatkuasa\s*:\s*(\d{1,2}/\d{1,2}/\d{4})", text)
        end = re.search(r"Tarikh Habis Tempoh Perakuan\s*:\s*(\d{1,2}/\d{1,2}/\d{4})", text)

        company_name = company.group(1).strip() if company else "Not Found"
        start_date = start.group(1) if start else "Not Found"
        end_date = end.group(1) if end else "Not Found"

        data_rows.append((company_name, start_date, end_date))

# Write to CSV
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data_rows)

print(f"✅ CSV report saved as '{output_csv}'")
