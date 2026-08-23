
import re
from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path
import os
from streamlit.string_util import clean_text
import tiktoken
from llm_model import model
from llm_setup_for_web_page import ask_llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate, SystemMessagePromptTemplate,MessagesPlaceholder
# loader = PyMuPDFLoader('pdf/health supplements/1. dietary supplements - for whom.pdf')

# docs = loader.load()

# print(f'Pdf content {docs[16].metadata}')
pdfs = []

for root,dirs,files in os.walk("pdf"):
    # print(f" file are {root} dire {dirs} files {files}")
    for file in files:
        if file.endswith('.pdf'):
            pdfs.append(file)

# print(f" pdf are --> {pdfs}\n")
docs = []



def format_docs(docs):
    return "\n\n".join([x.page_content for x in docs])      



# 1. Setup paths and tokenizer
pdf_dir = Path("pdf")
tokenizer_engine = tiktoken.encoding_for_model("gpt-4o-mini")

# Master lists to hold your data
all_cleaned_tokens = []
total_token_count = 0

# 2. Loop through every PDF file in all subfolders
for pdf_path in pdf_dir.rglob("*.pdf"):
    # print(f"Processing file: {pdf_path}")
    
    try:
        # Load the current PDF file (returns a list of pages)
        loader = PyMuPDFLoader(str(pdf_path))
        pages = loader.load()
        temp = pages
        docs.extend(temp)
        
        # 3. Loop through every individual page inside this specific PDF
        for page in pages:
            raw_text = page.page_content
            
            if not raw_text or not isinstance(raw_text, str):
                print("skipping page --> {page}")
                continue  # Skip empty or corrupted pages
                
            # 4. Apply your Regex cleaning patterns here
            # Pattern A: Replace multiple spaces/newlines with a single space
            # cleaned_text = re.sub(r'\s+', ' ', raw_text)
            cleaned_text = raw_text
            # Pattern B: Remove messy non-ASCII symbols/artifacts common in PDFs
            # cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)
            
            # cleaned_text = cleaned_text.strip()
            
            # 5. Tokenize the cleaned text
            if cleaned_text:
                page_tokens = tokenizer_engine.encode(cleaned_text)
                
                # Append to your master token list
                all_cleaned_tokens.extend(page_tokens)
                
                # Track the total count (safe loop if your len() function is still broken)
                for _ in page_tokens:
                    total_token_count += 1
                    
    except Exception as e:
        print(f"Error reading {pdf_path.name}: {e}")
        continue

# print("\n--- Processing Complete ---")
# print(f"Total cleaned tokens across ALL PDFs: {total_token_count}")
context = format_docs(docs)
len = len(docs)
# print(f"len {len}")
## LLM setup 

system = SystemMessagePromptTemplate.from_template('''You are helpful AI assistant who answer user question based on provided context. Do not answer in more than {words} words''') 
user_prompt = """Answer user question based on provide context ONLY. If you do not know the answer. Just say, "I do not know the answer".### Context: {context} ### Question: {question} ### Answer: """
prompt = HumanMessagePromptTemplate.from_template(user_prompt)

message = [system,prompt]

template = ChatPromptTemplate(message)

qna_chain = template | model | StrOutputParser()
# print(qna_chain)
u_ques = 'Examine the context and re-write the Profile Summary'
response = qna_chain.invoke({'context': context,'question':u_ques ,'words':200})
print(f"response is --> {response}")

