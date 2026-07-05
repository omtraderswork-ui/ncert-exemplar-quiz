import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
from transformers import pipeline

st.title("📘 AI Powered NCERT Exemplar Quiz")

pdf_file = st.file_uploader("Upload PDF", type="pdf")
if pdf_file:
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                img = page.to_image(resolution=200).original
                text += pytesseract.image_to_string(img)

    st.success("✅ Text extracted successfully!")

    # Use text2text-generation pipeline instead of question-generation
    qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-small-qa-qg-hl")

    # Generate MCQs from first 2000 chars of text
    context = text[:2000]
    output = qg_pipeline(context, max_length=256, do_sample=False)

    st.write("📊 AI Generated Questions:")
    for idx, q in enumerate(output):
        st.write(f"Q{idx+1}: {q['generated_text']}")
