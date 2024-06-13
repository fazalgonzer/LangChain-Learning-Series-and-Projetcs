import streamlit as st
import os 
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
load_dotenv()


groq_api_key=os.getenv('GROQ_API_KEY')
llm=ChatGroq(groq_api_key=groq_api_key,
            
             model_name="Llama3-8b-8192")

if "vector" not in st.session_state:
    st.session_state.embeddings=HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    st.session_state.loader=WebBaseLoader("https://python.langchain.com/v0.1/docs")
    st.session_state.load=st.session_state.loader.load()
    st.session_state.splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    st.session_state.docs=st.session_state.splitter.split_documents(st.session_state.load)
    st.session_state.vectors=FAISS.from_documents(st.session_state.docs,st.session_state.embeddings)

st.title("ChatGroq End ")

prompt=ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}

"""
)

document_chain=create_stuff_documents_chain(llm,prompt=prompt)
retriver=st.session_state.vectors.as_retriever()
retrival_chain=create_retrieval_chain(retriver,document_chain)
import time 
prompt=st.text_input("input your text here")
if prompt:
    start=time.process_time()
    response=retrival_chain.invoke({"input":prompt})
    print("Response Time :",time.process_time()-start)
    st.write(response['answer'])
    with st.expander("Document with similarity Search"):
        for i ,doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("------------------------")

