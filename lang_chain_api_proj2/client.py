import requests
import streamlit as st 

def get_essay_response(input_text):
    response=requests.post("http://localhost:8000/essay/invoke",
    json={'input':{'topic':input_text}})

    return response.json()['output']['content']




def get_poem_response(input_text):
    response=requests.post(
    "http://localhost:8000/poem/invoke",
    json={'input':{'topic':input_text}})

    return response.json()['output']['content']



#streamlit Framework
st.title('Langchain With LAMA AND Fast Api')
input_text1=st.text_input("write an essay on")
input_text2=st.text_input("write a poem on")

if input_text1:
    st.write(get_essay_response(input_text1))


if input_text2:
    st.write(get_poem_response(input_text2))
