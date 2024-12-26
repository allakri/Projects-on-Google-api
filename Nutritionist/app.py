import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini with API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input_text, image, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text, image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"An error occurred while getting the response: {str(e)}")
        return None

# Function to set up image for Gemini API
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the image file as bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app setup
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health Management App")

# Text input for user prompt
input_prompt = st.text_input("Enter additional instructions (optional)", key="input")

# File uploader for the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Button to trigger calorie analysis
submit_button = st.button("Calculate Total Calories")

# Prompt for nutritionist to calculate calories and provide details
nutritionist_prompt = """
You are an expert nutritionist with extensive knowledge of food items and their caloric values. Your task is to analyze the provided image of food items and identify each one. For every food item you recognize, please calculate its calorie content.
Instructions:
Carefully examine the image to identify all distinct food items.
For each identified food item, provide:
The name of the item
The corresponding calorie count
At the end of your analysis, calculate and present the total calorie count for all items combined.
Format your response as follows:
Item 1 - calories
Item 2 - calories
Item 3 - calories
...
Total Calorie Count: total calories
"""

# If submit button is clicked, process the image and get the response
if submit_button:
    if uploaded_file is not None:
        # Prepare the image for processing
        image_data = input_image_setup(uploaded_file)
        # Get response from the Gemini API
        response = get_gemini_response(input_prompt, image_data, nutritionist_prompt)

        # Display the response from Gemini
        if response:
            st.subheader("Calorie Analysis Result:")
            st.write(response)
        else:
            st.error("Unable to get a valid response. Please try again.")
    else:
        st.error("Please upload an image of the food items.")

