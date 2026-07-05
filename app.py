import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import re

st.title("📘 AI Powered NCERT Quiz")

pdf_file = st.file_uploader("Upload PDF", type="pdf")
if pdf_file:
    text = ""

    # Try extracting text with pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                # If no text, use OCR
                img = page.to_image(resolution=200).original
                text += pytesseract.image_to_string(img)

    st.success("✅ Text extracted successfully!")

    # AI/NLP step (simplified demo: regex for Q + options)
    raw_questions = re.findall(r'Q\d+\..*?(?=Q\d+\.|$)', text, re.S)
    questions = []
    for q in raw_questions:
        q = q.strip()
        q_lines = q.split("\n")
        question_text = q_lines[0]
        options = re.findall(r'\([a-d]\)\s.*', q)
        if len(options) == 4:
            questions.append({"q": question_text, "options": options, "answer": 0})

    if questions:
        score = 0
        for idx, q in enumerate(questions[:5]):
            st.write(f"Q{idx+1}: {q['q']}")
            choice = st.radio("Select one:", q["options"], key=idx)
            if st.button(f"Submit Q{idx+1}", key=f"btn{idx}"):
                if q["options"].index(choice) == q["answer"]:
                    st.success("Correct!")
                    score += 1
                else:
                    st.error("Wrong!")
        st.write("📊 Exam Finished!")
        st.write(f"Score: {score}/{len(questions[:5])}")
    else:
        st.warning("⚠️ No questions found. PDF format may need advanced NLP parsing.")
