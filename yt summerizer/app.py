import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()  # Load environment variables from a .env file

# Configure the Gemini API with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Updated prompt for YouTube video summarization
prompt = """
You are a YouTube video summarizer with expertise in extracting key insights from video transcripts. Your task is to summarize the transcript of a YouTube video into concise, easy-to-understand points, keeping the summary within 250 words.
Instructions:
Read the Transcript: Carefully analyze the provided transcript to understand the main themes and ideas presented in the video.
Extract Key Insights: Identify and highlight the most important points, concepts, or arguments made in the video.
Structure Your Summary:
Begin with a brief introduction that captures the overall theme of the video.
List the main ideas in bullet points or numbered format for clarity.
Conclude with a final thought or takeaway that encapsulates the essence of the video.
"""

# Function to extract the transcript details from a YouTube video using the YouTube Transcript API
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]  # Extract video ID from the URL
        # print(video_id)
        # Fetch the transcript using the video ID
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine all text segments into one string
        transcript = ""
        for segment in transcript_text:
            transcript += " " + segment["text"]

        return transcript

    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None

# Function to generate the summarized content from Gemini API
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

# Streamlit App UI setup
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

# If YouTube link is provided, display the video thumbnail
if youtube_link:
    try:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except IndexError:
        st.error("Invalid YouTube URL. Please ensure it contains a video ID.")

# When the user clicks on "Get Detailed Notes" button
if st.button("Get Detailed Notes"):
    if youtube_link:
        # Extract the transcript
        transcript_text = extract_transcript_details(youtube_link)

        # If transcript is extracted successfully, generate summary
        if transcript_text:
            with st.spinner("Generating summary..."):
                summary = generate_gemini_content(transcript_text, prompt)
                
                if summary:
                    st.markdown("## Detailed Notes:")
                    st.write(summary)
                else:
                    st.error("Could not generate summary. Please try again later.")
        else:
            st.error("Transcript extraction failed. Please check the video and try again.")
    else:
        st.error("Please provide a valid YouTube video link.")
