import streamlit as st
from PyPDF2 import PdfReader

st.title("📘 NCERT Exemplar Quiz Generator")

st.write("Welcome! Upload your Exemplar PDF to start the exam.")

pdf_file = st.file_uploader("Upload PDF", type="pdf")
if pdf_file:
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    st.success("✅ PDF uploaded successfully!")
    st.write("Sample extracted text:")
    st.write(text[:500])  # demo output

    # Exam start instructions
    st.info("Exam starts now! You have 30 minutes.")

    # Demo quiz question
    st.write("Q1: Which law explains the relation between force and acceleration?")
    if st.button("Newton’s First Law"):
        st.error("Wrong!")
    if st.button("Newton’s Second Law"):
        st.success("Correct!")
    if st.button("Newton’s Third Law"):
        st.error("Wrong!")
    if st.button("Law of Gravitation"):
        st.error("Wrong!")

    # End analysis
    st.write("📊 Exam Finished! Score: 1/1")
    st.write("🏆 Rank: Top 10%")
