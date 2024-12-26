from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image, UnidentifiedImageError
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input_text, image, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Updated to the supported model
        response = model.generate_content([input_text, image[0], prompt])
        return response.text
    except Exception as e:
        st.error("An error occurred while fetching the response from the Gemini API.")
        raise e

# Function to handle uploaded image
def input_image_setup(uploaded_file):
    try:
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = [
                {
                    "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                    "data": bytes_data
                }
            ]
            return image_parts
        else:
            st.error("Please upload an image.")
            raise FileNotFoundError("No file uploaded")
    except UnidentifiedImageError:
        st.error("The uploaded file is not a valid image.")
        raise

# Streamlit app setup
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

# Input fields
input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    except UnidentifiedImageError:
        st.error("The uploaded file could not be opened as an image.")

# Submission button
submit = st.button("Tell me about the image")

# Input prompt for Gemini
input_prompt = """
You are an expert in understanding invoices.
You will receive input images as invoices &
you will have to answer questions based on the input image.
"""

# Handle button click
if submit:
    if not input_text.strip():
        st.error("Input prompt cannot be empty. Please provide a valid prompt.")
    elif uploaded_file is None:
        st.error("Please upload an image before submitting.")
    else:
        try:
            with st.spinner("Processing... Please wait."):
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_text, image_data, input_prompt)
                st.subheader("The Response is")
                st.write(response)
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
