# src/app.py
import streamlit as st
from ocr_extraction import extract_text_from_image
from ingredient_classifier import classify_ingredients
import os

st.set_page_config(page_title="Food Authenticity Checker", layout="centered")
st.title("🍴 Food Authenticity Checker (Veg / Non-Veg)")

uploaded = st.file_uploader("Upload a food label image", type=["jpg", "jpeg", "png"])

if uploaded is not None:
    # save temporary file
    temp_path = "temp_upload.jpg"
    with open(temp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.image(temp_path, caption="Uploaded label", use_column_width=True)

    # run OCR
    with st.spinner("Reading text from the image..."):
        try:
            extracted = extract_text_from_image(temp_path)
        except Exception as e:
            st.error(f"OCR failed: {e}")
            extracted = ""

    st.subheader("Extracted text (edit if it's wrong):")
    edited = st.text_area("OCR result (you can fix typos here)", value=extracted, height=150)

    if st.button("Classify ingredients"):
        label, reasons, confidence = classify_ingredients(edited)
        if "Non-Vegetarian" in label:
            st.error(label)
        elif "Vegetarian" in label:
            st.success(label)
        else:
            st.warning(label)

        if reasons:
            st.write("Detected words:", ", ".join(reasons))
        st.write("Match count (higher is more sure):", confidence)

        # Save a small log for yourself
        os.makedirs("results", exist_ok=True)
        with open("results/log.txt", "a", encoding="utf-8") as log:
            log.write(f"file:{uploaded.name} => label:{label} reasons:{reasons}\n")

    st.markdown("---")
    st.info("If classification is unclear, edit the extracted text above and press the button again.")
