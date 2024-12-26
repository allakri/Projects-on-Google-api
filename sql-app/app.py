import os
import sqlite3
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Check if the API key is available
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key not found in the environment variables!")
else:
    # Configure Genai with API Key
    genai.configure(api_key=api_key)

# Function to get response from Gemini model
def get_gemini_response(question, prompt):
    try:
        # Use the 'gemini-pro' model to generate content based on the prompt and question
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])
        return response.text.strip()
    except Exception as e:
        st.error(f"Error getting response from Gemini model: {e}")
        return None

# Function to execute SQL query and return results
def read_sql_query(sql, db):
    try:
        # Connect to the SQLite database and execute the query
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        st.error(f"SQLite error: {e}")
        return []

# Define your updated prompt for Gemini model
prompt = [
    """
    You are an expert in converting natural language questions into SQL queries for a database. The database is named 'college.db' and contains a table named 'COLLEGES' with the following columns:
    - name (TEXT): The name of the college.
    - courses (TEXT): A list of courses offered by the college.
    - rating (REAL): The rating of the college.
    - fee (INTEGER): The fee structure of the college.

    Handle various types of queries as follows:
    1. Basic Queries: Convert straightforward questions into SQL.
    2. Ambiguous Queries: Make assumptions or request more details.
    3. Typos and Misspellings: Correct common errors.
    4. Non-Standard Queries: Infer the most likely intent.

    Examples:
    - "What is the fee structure for Tech University?" should be converted to:
      SELECT fee FROM COLLEGES WHERE name = "Tech University";
      
    - "Colleges with high ratings?" should be converted to:
      SELECT name FROM COLLEGES WHERE rating > 4.0;

    - "Find the cheapest college with computer science?" should be converted to:
      SELECT name FROM COLLEGES WHERE courses LIKE "%Computer Science%" ORDER BY fee ASC LIMIT 1;

    Ensure that the SQL query does not include any delimiters like ``` and does not use the word 'SQL' in the output.
    """
]

# Streamlit App Interface
st.set_page_config(page_title="Gemini SQL Query App", layout="wide")
st.header("Chatbot Q & A Session")

question = st.text_input("Enter your question about the college database:", key="input")
submit = st.button("Ask the question")

# Use session_state to track if the query has been processed
if 'sql_query_generated' not in st.session_state:
    st.session_state.sql_query_generated = False

# Handle user input and submission
if submit:
    if question:
        # Generate SQL query only if it's not already done
        if not st.session_state.sql_query_generated:
            # Get the SQL query from Gemini
            sql_query = get_gemini_response(question, prompt)

            # If a valid SQL query was returned, execute it
            if sql_query:
                st.session_state.sql_query = sql_query  # Save the query in session state
                st.session_state.sql_query_generated = True  # Mark the query as generated
                st.write(f"Generated SQL Query: {sql_query}")  # Display the generated SQL query for debugging

                # Retrieve data from database
                try:
                    response = read_sql_query(sql_query, "college.db")

                    # Display query results
                    st.subheader("Query Results:")
                    if response:
                        for row in response:
                            st.write(row)
                    else:
                        st.write("No data found or invalid query.")
                except Exception as e:
                    st.error(f"An error occurred while executing the query: {e}")
        else:
            # If the SQL query was already generated, just display the results
            st.write(f"Generated SQL Query: {st.session_state.sql_query}")
            st.subheader("Query Results:")
            response = read_sql_query(st.session_state.sql_query, "college.db")
            if response:
                for row in response:
                    st.write(row)
            else:
                st.write("No data found or invalid query.")
    else:
        st.warning("Please enter a question.")

