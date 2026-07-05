import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
from transformers import pipeline
import time

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

    # HuggingFace Question Generation pipeline
    qg_pipeline = pipeline("question-generation", model="valhalla/t5-small-qa-qg-hl")

    # Generate MCQs from first 3000 chars of text
    context = text[:3000]
    questions = qg_pipeline(context)

    if questions:
        # Timer setup
        if "start_time" not in st.session_state:
            st.session_state.start_time = time.time()
        elapsed = int(time.time() - st.session_state.start_time)
        st.write(f"⏳ Time elapsed: {elapsed} seconds")

        score = 0
        for idx, q in enumerate(questions[:5]):  # show first 5 questions
            st.write(f"Q{idx+1}: {q['question']}")
            options = q.get("options", ["Option A","Option B","Option C","Option D"])
            choice = st.radio("Select one:", options, key=idx)
            if st.button(f"Submit Q{idx+1}", key=f"btn{idx}"):
                st.info("Answer checking demo — correct answer mapping needed")
                # Placeholder: you can add answer key logic here

        st.write("📊 Exam Finished!")
        st.write(f"Score: {score}/{len(questions[:5])}")
        st.write("🏆 Rank analysis: Demo Top 20%")
    else:
        st.warning("⚠️ No questions generated. Try uploading a different PDF or increase context size.")
