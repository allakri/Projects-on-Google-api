import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Gemini with API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Define a prompt template for ATS evaluation
input_prompt_evaluation = """
You are a skilled ATS (Applicant Tracking System) with expertise in the tech field, including software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the given resume based on the provided job description. 
The job market is competitive, and you should provide the best assistance in improving the resume. 

Resume: {text}
Job Description: {jd}

Provide the following:
- Matching Percentage between the resume and job description.
- Missing Keywords (if any) in the resume.
- A brief Profile Summary for improvement suggestions.

Response Format:
{{"JD Match":"%", "Missing Keywords":[], "Profile Summary":""}}
"""

# Define a prompt template for skill improvement suggestions and roadmap
input_prompt_skill_improvement = """
You are a career expert and an ATS consultant with a deep understanding of the tech industry. Your task is to evaluate the provided job description and suggest the key skills required for the role. 
Additionally, provide a roadmap for improving these skills for the candidate's profile.

Job Description: {jd}

Provide:
- A list of skills required for the job role.
- A clear roadmap to acquire these skills (with steps).
"""

# Define a prompt for ATS evaluation with improvement roadmap
input_prompt_roadmap = """
You are a skilled ATS with knowledge of the tech industry, particularly in software engineering, data science, data analysis, and big data engineering. Your task is to evaluate a resume against the given job description, 
and then provide a roadmap for improvement.

Resume: {text}
Job Description: {jd}

Provide:
- Matching percentage between resume and job description.
- Missing Keywords.
- Profile Summary.
- Skill improvement roadmap to enhance the profile for the role.
"""

# Streamlit App
st.title("Smart ATS - Resume Improvement Assistant")
st.text("Enhance your resume by analyzing your skills against the job description")

# Input fields
jd = st.text_area("Paste the Job Description here")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload your resume in PDF format.")

# Buttons for different actions
submit_evaluation = st.button("Evaluate Resume against Job Description")
submit_skill_improvement = st.button("Skill Improvement Suggestions")
submit_roadmap = st.button("Generate Improvement Roadmap")

# Handle button actions
if submit_evaluation:
    if uploaded_file is not None and jd:
        text = input_pdf_text(uploaded_file)
        input_text = input_prompt_evaluation.format(text=text, jd=jd)
        response = get_gemini_response(input_text)
        try:
            # Try parsing the response as JSON
            response_data = json.loads(response)
            st.subheader("Evaluation Results:")
            st.write(f"JD Match: {response_data.get('JD Match', 'N/A')}")
            st.write(f"Missing Keywords: {', '.join(response_data.get('Missing Keywords', []))}")
            st.write(f"Profile Summary: {response_data.get('Profile Summary', 'N/A')}")
        except json.JSONDecodeError:
            # If response is not in JSON format, show raw text response
            st.error("Failed to decode the response. Showing raw output:")
            st.write(response)

elif submit_skill_improvement:
    if uploaded_file is not None and jd:
        input_text = input_prompt_skill_improvement.format(jd=jd)
        response = get_gemini_response(input_text)
        st.subheader("Skill Improvement Suggestions:")
        st.write(response)

elif submit_roadmap:
    if uploaded_file is not None and jd:
        text = input_pdf_text(uploaded_file)
        input_text = input_prompt_roadmap.format(text=text, jd=jd)
        response = get_gemini_response(input_text)
        try:
            # Try parsing the response as JSON
            response_data = json.loads(response)
            st.subheader("Improvement Roadmap:")
            st.write(f"JD Match: {response_data.get('JD Match', 'N/A')}")
            st.write(f"Missing Keywords: {', '.join(response_data.get('Missing Keywords', []))}")
            st.write(f"Profile Summary: {response_data.get('Profile Summary', 'N/A')}")
            st.write(f"Skill Improvement Roadmap: {response_data.get('Skill Improvement Roadmap', 'N/A')}")
        except json.JSONDecodeError:
            # If response is not in JSON format, show raw text response
            st.error("Failed to decode the response. Showing raw output:")
            st.write(response)

# Error handling for missing file or job description
else:
    if uploaded_file is None:
        st.warning("Please upload a resume.")
    if not jd:
        st.warning("Please enter a job description.")
