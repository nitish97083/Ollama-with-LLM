import asyncio
import re
from langchain_community.document_loaders import WebBaseLoader

import llm_setup_for_web_page as lswp

urls = [
    #  'https://www.screener.in/company/SALZERELEC/#quarters',
    #    'https://www.moneycontrol.com/news/business/stocks/',
    #   'https://economictimes.indiatimes.com/markets/stocks/news',
      'https://groww.in/market-news/stocks',
    
        ]

loader = WebBaseLoader(web_paths=urls)

docs = []

# async for doc in loader.alazy_load():
#     docs.append(doc)
    
async def load_docs():
    
    async for doc in loader.alazy_load():
        docs.append(doc)
    return docs


docs = asyncio.run(load_docs())
# print(docs[0].page_content)   
   
def document_format(docs):
    return "\n\n".join([x.page_content for x in docs])   


context = document_format(docs)   

def clean_text(text):
   text =  re.sub(r'\n\n+', '\n\n', text)
   text = re.sub(r'\t+', '\t',text)
   text = re.sub(r'\s+',' ',text)
   return text

formated_text = clean_text(context)
leng = len(formated_text)
print(f"len {leng}") 


def chunk_text(text,chunk_size,overlap =200):
    chunks = []
    for i in range(0,len(text),chunk_size-overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks    
re_ques = 'Write a detailed report in Markdown from the given context'
chunks = chunk_text(formated_text,8_000)     

response = lswp.ask_llm(formated_text[1_000:8_000],re_ques)
print(f"response is --> {response}")
