import streamlit as st
import pdfplumber
import re

st.title("📘 NCERT Exemplar Quiz Generator")

pdf_file = st.file_uploader("Upload NCERT Exemplar PDF", type="pdf")
if pdf_file:
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    st.success("✅ PDF uploaded successfully!")

    # Extract question blocks: look for "Q1.", "Q2." etc.
    raw_questions = re.findall(r'Q\d+\..*?(?=Q\d+\.|$)', text, re.S)

    questions = []
    for q in raw_questions:
        q = q.strip()
        # Question text = first line before options
        q_lines = q.split("\n")
        question_text = q_lines[0]

        # Options: look for (a), (b), (c), (d)
        options = re.findall(r'\([a-d]\)\s.*', q)
        if len(options) == 4:
            questions.append({
                "q": question_text,
                "options": options,
                "answer": 0  # placeholder
            })

    if not questions:
        st.warning("⚠️ No questions found. Try checking PDF formatting.")
    else:
        score = 0
        for idx, q in enumerate(questions[:5]):  # show first 5 questions
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
