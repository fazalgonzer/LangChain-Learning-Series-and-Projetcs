import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
env_path = 'lang_chain_1_proj1\.env'
load_dotenv(dotenv_path=env_path)

os.environ["CHATGROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
groq_api_key=os.getenv('GROQ_API_KEY')

prompt=ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "Question:{question}")
])

st.title('LAngchain with GroqApiKey')
input_text=st.text_input("Search the topic you want to search")


llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192")

output_parser=StrOutputParser()
chain=prompt|llm|output_parser
if input_text:
    st.write(chain.invoke({'question':input_text}))
