import os
import warnings
from langchain_community.docstore import InMemoryDocstore

from llm_model import model



os.environ['KMP_DUPLICATE_LIB_OK']='True'

warnings.filterwarnings('ignore')

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate




prompt = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Answer in bullet points. Make sure answer is relevant to the question and it is answerred from context only.
Question: {question} 
Context: {context} 
Answer:
"""
chat_tem_prompt = ChatPromptTemplate.from_template(prompt)
    
base_url = "http://localhost:11434";
base_model= "nomic-embed-text"    


emebedings = OllamaEmbeddings(model= base_model,base_url=base_url)

db_name = 'health_supplements'

vector_search = FAISS.load_local(db_name,
                                 emebedings,
                                 allow_dangerous_deserialization=True
                                 )


# docs =vector_search.search(query=question,k=5,search_type= 'similarity')

retriver = vector_search.as_retriever(
    search_type= 'similarity',
    search_kwargs = {'k':3}
                 )

# response_docs = retriver.invoke(question)
# print(f'response  is {response_docs}')


def format_docs(docs):
    return '\n\n'.join([doc.page_content for doc in docs])

# context_data = format_docs(response_docs)

# print(context_data)

rag_chain = (
    {'context': retriver|format_docs , 'question':RunnablePassthrough()}
    | chat_tem_prompt | model |StrOutputParser() 
)

question = ['how to lose weight?','How to gain mass muscle?']
llm_res = rag_chain.invoke(question[1])

print(f"Response is \n {llm_res}")
