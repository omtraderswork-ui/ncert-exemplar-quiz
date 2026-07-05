import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
from transformers import pipeline

st.title("📘 AI Powered NCERT Quiz")

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

    # HuggingFace NLP model for question generation
    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

    # Example: generate one demo question from extracted text
    context = text[:1000]  # take first 1000 chars
    question = "What is the main concept explained?"
    result = qa_pipeline(question=question, context=context)

    st.write("Sample AI Generated Question:")
    st.write(question)
    st.write("Answer:", result['answer'])
