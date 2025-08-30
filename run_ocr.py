# run_ocr.py
from src.ocr_extraction import extract_text_from_image

path = "data/sample_labels/label1.jpg"
text = extract_text_from_image(path)
print("----- OCR Result -----")
print(text)
print("----------------------")
