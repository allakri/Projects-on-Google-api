import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import time

# Load the environment variables
load_dotenv()

# Load the API keys
groq_api_key = os.getenv('GROQ_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize the model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

st.title("Career Guidance Chatbot")

# Chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Define prompt template
prompt = ChatPromptTemplate.from_template(
    """
    You are a career guidance counselor.
    Help the student choose their next educational step based on their interests and academic performance.
    Engage in a conversation to understand their preferences.
    Answer the question below with accurate information:
    
    Context:
    {context}
    
    Question: {input}
    """
)

# Function to store chat history
def store_chat(user_input, bot_response):
    st.session_state.history.append({"user": user_input, "bot": bot_response})

# Function to load embeddings
def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader = PyPDFDirectoryLoader("./education")  # Data ingestion
        st.session_state.docs = st.session_state.loader.load()  # Document loading
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Chunking
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:20])
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# Get user input
user_input = st.text_input("Ask your career-related question:")

# Display chat history
for chat in st.session_state.history:
    st.write(f"You: {chat['user']}")
    st.write(f"Bot: {chat['bot']}")

# Button to process embeddings
if st.button("Documents Embedding"):
    vector_embedding()
    st.write("Vector Store DB is ready")

# Process user input
if user_input:
    vector_embedding()  # Ensure vector embeddings are loaded
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Retrieve response
    start = time.process_time()
    response = retrieval_chain.invoke({'input': user_input})
    end_time = time.process_time() - start

    bot_response = response['answer']
    st.write(f"Bot: {bot_response}")
    store_chat(user_input, bot_response)

    # # Expand document similarity search
    # with st.expander("Document Similarity Search"):
    #     for doc in response.get("context", []):
    #         st.write(doc.page_content)
    #         st.write("--------------------------------")
