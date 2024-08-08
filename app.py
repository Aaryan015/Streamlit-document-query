import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PyPDF2 import PdfReader
from docx import Document
from cryptography.fernet import Fernet

# Create the uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Database setup
DATABASE_URL = "sqlite:///documents.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Encryption setup
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Models
class DocumentModel(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    content = Column(String)

class UserHistory(Base):
    __tablename__ = "user_history"
    id = Column(Integer, primary_key=True)
    user = Column(String)
    query = Column(String)
    response = Column(String)

Base.metadata.create_all(engine)

# Functions to read different document formats
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

def read_txt(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    return text

# Function to encrypt content
def encrypt_content(content):
    return cipher_suite.encrypt(content.encode()).decode()

# Function to decrypt content
def decrypt_content(encrypted_content):
    return cipher_suite.decrypt(encrypted_content.encode()).decode()

# Function to save uploaded files
def save_uploadedfile(uploadedfile):
    with open(os.path.join("uploads", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved file :{} in uploads folder".format(uploadedfile.name))

# Function to search documents
def search_documents(query, file_path):
    if file_path.endswith(".pdf"):
        text = read_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = read_docx(file_path)
    else:
        text = read_txt(file_path)
    
    if query.lower() in text.lower():
        return True, text
    else:
        return False, ""

# Function to save user history
def save_user_history(user, query, response):
    history = UserHistory(user=user, query=query, response=response)
    session.add(history)
    session.commit()

# Function to get user history
def get_user_history(user):
    return session.query(UserHistory).filter_by(user=user).all()

# Function to save history to file
def save_history_to_file(user):
    history = get_user_history(user)
    with open(f"{user}_history.txt", "w") as file:
        for record in history:
            file.write(f"Query: {record.query}\nResponse: {record.response}\n\n")

# Streamlit UI
st.title("Document Query Application")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    save_uploadedfile(uploaded_file)
    # Encrypt and save file details to database
    content = ""
    if uploaded_file.name.endswith(".pdf"):
        content = read_pdf(os.path.join("uploads", uploaded_file.name))
    elif uploaded_file.name.endswith(".docx"):
        content = read_docx(os.path.join("uploads", uploaded_file.name))
    else:
        content = read_txt(os.path.join("uploads", uploaded_file.name))
    
    encrypted_content = encrypt_content(content)
    document = DocumentModel(filename=uploaded_file.name, content=encrypted_content)
    session.add(document)
    session.commit()

query = st.text_input("Enter your query:")
search_results = []

if st.button("Search"):
    with engine.connect() as conn:
        result = conn.execute("SELECT filename, content FROM documents").fetchall()
        for row in result:
            file_path = os.path.join("uploads", row[0])
            decrypted_content = decrypt_content(row[1])
            found = query.lower() in decrypted_content.lower()
            if found:
                search_results.append((row[0], decrypted_content))
    
    if search_results:
        st.write("Found in the following documents:")
        for filename, text in search_results:
            st.write(f"Document: {filename}")
            st.write(text[:500])  # Display first 500 characters
            save_user_history("test_user", query, text[:500])
    else:
        st.write("No results found.")

if st.button("Download chat history"):
    save_history_to_file("test_user")
    st.download_button(
        label="Download chat history",
        data=open("test_user_history.txt", "rb").read(),
        file_name="test_user_history.txt"
    )
