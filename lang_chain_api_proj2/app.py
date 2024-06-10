from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langserve import add_routes
import uvicorn
import os 
from dotenv import load_dotenv

env_path = 'lang_chain_api_proj2\.env'
load_dotenv(dotenv_path=env_path)

os.environ["CHATGROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
groq_api_key=os.getenv('GROQ_API_KEY')

#defining model :
llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192") 

app=FastAPI(
   title="Langchain Server",
   version="1.0",
   description="A simple Api Server"

)
prompt1=ChatPromptTemplate.from_template("Write me an essay {topic} with 100 Words ")
prompt2=ChatPromptTemplate.from_template("Write me an poem {topic} with 100 Words ")


add_routes(app,
           prompt1|llm,
           path="/essay"
           )


add_routes(app,
           prompt2|llm,
           path="/poem"
           )

if __name__== "__main__":
    uvicorn.run(app,host="localhost",port=8000)