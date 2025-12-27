import streamlit as st
import PyPDF2
import os
import io
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="KNOW YOUR RESUME", page_icon="🔍", layout="centered")

st.title("KNOW YOUR RESUME 🔍")
st.markdown("upload your resume and get ai powered feed back about it")

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("upload your resume for analysis",type =["pdf","docx"])
job_role = st.text_input("Enter the job role you are applying for:")
analyze = st.button("Analyze Resume")

def analyze_resume_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def analyze_resume_from_file(uploaded_file):
   if uploaded_file.type == "application/pdf":
        return analyze_resume_from_pdf(io.BytesIO(uploaded_file.read()))
   return uploaded_file.read().decode("utf-8")

 

if analyze and uploaded_file:
  try:
    file_content = analyze_resume_from_file(uploaded_file)

    if not file_content.strip():
        st.error("file is empty")
        st.stop()

    prompt = f"""please analyze this resume and provide feedback on how to improve it for future applications.
    focus on the following aspects:
    1. content clarity and impact    
    2. skills presentation
    3. experience description
    4. chances of acceptance for the current experience and skills
    5. resume score based on industry standards
    6. tailoring to the job role of {job_role if job_role else 'general applicatons'}

    resume content:
    {file_content}

    please provide your feedback and analysis in a structured format with clear sections for each aspect mentioned above."""

    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert resume critiquer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    st.markdown("### Here is your result after analysis:")
    st.markdown(response.choices[0].message.content)
  except Exception as e:
     st.error(f"An error has occurred: {str(e)}")