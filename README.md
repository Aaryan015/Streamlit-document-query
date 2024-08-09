# Document Query Application using Streamlit 🚀

## Overview📖
This application allows users to query documents to answer their questions. It supports .pdf, .docx, and .txt formats and maintains user history, providing an option to download chat history.
### Use the application [**here**](https://document-query-app.streamlit.app/)

## Features ✨
- Upload and query documents
- Securely store data in a database
- Maintain user interaction history
- Downloadable chat history
- User-friendly interface

## Setup Instructions 🗒️

### Prerequisites 👜
- Python 3.8+
- Pip

### Installation 🧰
1. Clone the repository
   ```sh
   git clone https://github.com/Aaryan015/Streamlit-document-query.git

2. Set up the virtual environment
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate
   ```
   **Note**: If you encounter an error like:
   ```
   running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
   At line:1 char:1
   + venv\Scripts\activate
   ```
   Follow these steps:
   1. Open PowerShell as Administrator and change the execution policy:
   ```sh
      Set-ExecutionPolicy RemoteSigned
   ```
   2. Type Y and press Enter.

   3. Activate the Virtual Environment:
   ```sh
   venv\Scripts\Activate.ps1
   
3. Install the dependencies
   ```sh
   pip install -r requirements.txt

4. Run the application
   ```sh
   streamlit run app.py
   ```
   ![refresh page](https://github.com/Aaryan015/Streamlit-document-query/blob/main/UI.png?raw=true)

### Security 🔐
- Data is encrypted using the cryptography library.
- User history is stored securely and accessible only to the respective user.

### Adding New Documents 📎
- Upload new documents using the document upload feature in the application.

### Deployment 🏃
- Deploy the application using your preferred platform. Please ensure to update the database URL and secrets accordingly.
