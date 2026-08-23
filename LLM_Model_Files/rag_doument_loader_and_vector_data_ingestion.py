import os
import warnings
from langchain_community.docstore import InMemoryDocstore
import tiktoken

from shapely import length
os.environ['KMP_DUPLICATE_LIB_OK']='True'

warnings.filterwarnings('ignore')

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import faiss
from langchain_community.vectorstores import FAISS

pdfs = []

for root, dirs,files in os.walk("rag-dataset"):
    # print(f" dirs is {files}")
    for file in files :
        if file.endswith('.pdf'):
            pdfs.append(os.path.join(root,file))
            
            
# print(f" pdf are {pdfs}")  

docs = []

for pdf in pdfs:
    loader = PyMuPDFLoader(pdf)
    temp = loader.load()
    docs.extend(temp)
len1 = len(docs)             
print(f"pegs are --> {len1}")        

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap = 100)

chunks = text_splitter.split_documents(docs);

# print(f"chunk are \n{chunks}")

encoding = tiktoken.encoding_for_model("gpt-4o-mini")
token = encoding.encode(docs[5].page_content)
count= 0
for i in token:
    count= count+1
    
base_url = "http://localhost:11434";
base_model= "nomic-embed-text"    
# print(f"count is {count} and ")

emebedings = OllamaEmbeddings(model= base_model,base_url=base_url)

vector = emebedings.embed_query("Hello world")

v_len = len(vector)
v_index = faiss.IndexFlatL2(v_len)

print(f"vector len {v_len}")

vector_store = FAISS(embedding_function= emebedings,
                     index= v_index,
                     docstore=InMemoryDocstore(),
                     index_to_docstore_id= {}
                     )



ids = vector_store.add_documents(documents=chunks)
        
print(f" vecotor {vector_store.index.ntotal} and ids len {len(ids)}")  

question = 'how to gain muscle mass?'

docs = vector_store.search(query=question,k=5,search_type= 'similarity')

print(docs[0].page_content)

db_name = 'health_supplements'

vector_store.save_local(db_name)

