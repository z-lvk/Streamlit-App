import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader


def configure_api_key():
    key = "AIzaSyBi9GZN04zfLfX1Zkyu7PU3FczkPTJAYeo"  
    os.environ['GOOGLE_API_KEY'] = key
    genai.configure(api_key=key)

def initialize_model():
    return genai.GenerativeModel('gemini-pro')


def display_messages(messages):
    for message in reversed(messages):
        if message["role"] == "assistant":
            st.warning("🤖 " + message["content"])
        else:
            st.info("👤 " + message["content"])


def process_query(query, model, uploaded_file_info, file_content, messages):
    try:
        if uploaded_file_info and "file" in query.lower():
            response = model.generate_content(query + " " + file_content).text
        else:
            response = model.generate_content(query).text

        if response:
            messages.append({"role": "user", "content": query})
            messages.append({"role": "assistant", "content": response})
        else:
            messages.append({"role": "assistant", "content": "I'm sorry, I couldn't generate a valid response for your query."})
    except Exception as e:
        st.error("An error occurred while processing your request. Please try again later.")
        messages.append({"role": "assistant", "content": "I encountered an error while processing your request."})


def process_uploaded_file(uploaded_file, uploaded_file_info, file_content):
    if uploaded_file:
        uploaded_file_info.update({
            "name": uploaded_file.name,
            "size": uploaded_file.size,
            "type": uploaded_file.type
        })

        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            file_content += page.extract_text()

        st.success("File uploaded successfully. (Include word 'file' to answer questions related to file)")
    return uploaded_file_info, file_content


def main():
    st.title("NovaNexus ☁️")

    
    configure_api_key()

    model = initialize_model()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    uploaded_file_info = {}
    file_content = ""


    query = st.text_input("Ask a question..")

    uploaded_file = st.sidebar.file_uploader("Upload a PDF file..", type="pdf")

    uploaded_file_info, file_content = process_uploaded_file(uploaded_file, uploaded_file_info, file_content)

    if query:
        process_query(query, model, uploaded_file_info, file_content, st.session_state.messages)

    display_messages(st.session_state.messages)


if __name__ == "__main__":
    main()






