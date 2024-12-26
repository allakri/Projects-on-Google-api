from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set up the Google API Key for Gemini Pro
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Generative Model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get a response from Gemini Pro model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app configuration
st.set_page_config(page_title="Q&A Demo", layout="wide")

# Custom CSS to style the app
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 65vh;
            overflow-y: auto;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #121212;
            color: white;
        }
        .chat-message {
            margin: 5px 0;
            display: flex;
            align-items: center;
        }
        .chat-message.user {
            justify-content: flex-end;
        }
        .chat-message.bot {
            justify-content: flex-start;
        }
        .chat-avatar {
            width: 30px;
            height: 30px;
            margin: 0 10px;
            border-radius: 50%;
        }
        .chat-bubble {
            max-width: 70%;
            padding: 10px;
            border-radius: 10px;
            background-color: #1f1f1f;
            color: white;
        }
        .chat-bubble.user {
            background-color: #007bff;
            color: white;
        }
        .chat-bubble.bot {
            background-color: #444;
            color: white;
        }
        .input-container {
            display: flex;
            align-items: center;
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 10px;
            background-color: #121212;
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.2);
        }
        .input-container input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #444;
            border-radius: 5px;
            background-color: #1f1f1f;
            color: white;
            margin-right: 10px;
        }
        .input-container button {
            background-color: #007bff;
            border: none;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .input-container button:hover {
            background-color: #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.header("Gemini LLM Search Assistant")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Chat history container
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, text in st.session_state['chat_history']:
    if role == "You":
        st.markdown(
            f"""
            <div class="chat-message user">
                <img src="https://cdn-icons-png.flaticon.com/512/3177/3177440.png" class="chat-avatar">
                <div class="chat-bubble user">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="chat-message bot">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712108.png" class="chat-avatar">
                <div class="chat-bubble bot">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
# st.markdown('</div>', unsafe_allow_html=True)

# # Input container
# st.markdown('<div class="input-container">', unsafe_allow_html=True)
# input_text = st.text_input("Ask a question:", key="input", label_visibility="collapsed")
# submit_button = st.button("➤", use_container_width=False)

import streamlit as st

# Create two columns for the input field and button to be on the same row
col1, col2 = st.columns([4, 1])  # Adjust the relative width of the columns

with col1:
    input_text = st.text_input("Ask a question:", key="input", label_visibility="collapsed")

with col2:
    submit_button = st.button("➤", use_container_width=False)

# Add some styling to the container if needed
st.markdown('<style>div.input-container { display: flex; }</style>', unsafe_allow_html=True)

if submit_button and input_text:
    response = get_gemini_response(input_text)
    st.session_state['chat_history'].append(("You", input_text))
    for chunk in response:
        st.session_state['chat_history'].append(("Bot", chunk.text))

st.markdown('</div>', unsafe_allow_html=True)

# Clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state['chat_history'] = []

# Footer
st.markdown("___")
st.markdown("Powered by Gemini Pro - Your AI Assistant.")
