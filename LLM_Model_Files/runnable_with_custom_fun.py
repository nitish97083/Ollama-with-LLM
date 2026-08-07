from llm_model import model;
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

user_prompt = '''answer the both  {input1} and {input2} in 3 line. separte with input and provide the answer in human readable format.'''

prompt_template = ChatPromptTemplate.from_template(user_prompt);

def word_count(words):
    return len(words.split())

def char_count(words):
    return len(words)

chain = prompt_template | model| StrOutputParser()|{'word_count':RunnableLambda(word_count), 
'char_count':RunnableLambda(char_count)
,'output':RunnablePassthrough()};
response = chain.invoke({'input1': 'About Sun', 'input2': 'About Earth'});
print(f"Word Count: {response['word_count']}");
print(f"\nCharacter Count: {response['char_count']}\n");
print(f"\nResponse: {response['output']}");
