import streamlit as st
from PyPDF2 import PdfReader
import re

st.title("📘 NCERT Exemplar Quiz Generator")

st.write("Upload your Exemplar PDF to start the exam.")

pdf_file = st.file_uploader("Upload PDF", type="pdf")
if pdf_file:
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    st.success("✅ PDF uploaded successfully!")

    # Simple regex to split questions (assuming "Q." or "Question" marks start)
    raw_questions = re.split(r'Q[0-9]+\.|Question', text)

    questions = []
    for q in raw_questions:
        q = q.strip()
        if len(q) > 20:  # filter out small junk
            # For demo, just take first sentence as question
            parts = q.split("\n")
            question_text = parts[0]
            options = parts[1:5]  # assume next 4 lines are options
            if len(options) == 4:
                questions.append({
                    "q": question_text,
                    "options": options,
                    "answer": 0  # placeholder, you can mark correct later
                })

    # Timer (simple countdown)
    if "time_left" not in st.session_state:
        st.session_state.time_left = 60

    st.write(f"⏳ Time left: {st.session_state.time_left} seconds")

    # Show questions
    score = 0
    for idx, q in enumerate(questions[:5]):  # show first 5 questions
        st.write(f"Q{idx+1}: {q['q']}")
        for i, opt in enumerate(q["options"]):
            if st.button(opt, key=f"{idx}-{i}"):
                if i == q["answer"]:
                    st.success("Correct!")
                    score += 1
                else:
                    st.error("Wrong!")

    # End analysis
    st.write("📊 Exam Finished!")
    st.write(f"Score: {score}/{len(questions[:5])}")
    st.write("🏆 Rank analysis: (demo) Top 20%")
