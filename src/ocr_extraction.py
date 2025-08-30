
import pytesseract
import cv2
import os
from PIL import Image



def extract_text_from_image(image_path):
   
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

  
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image (maybe wrong path or unsupported file).")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    text = pytesseract.image_to_string(thresh, lang='eng')  # 'eng' = English
    return text
