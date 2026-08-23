


from langchain_ollama import ChatOllama
import streamlit as st

from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    ChatPromptTemplate
)
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

## Model setup 

base_url = "http://localhost:11434";
model_man = "ManavEdu";
g_model = "gemma4"
llm = "llama3.2"


model = ChatOllama(
    base_url=base_url,
    model=model_man,
    #validate_model_on_init=True,
    temperature=0.8,
    num_predict=512,
    num_ctx=512,
    top_k=20,
    top_p=0.2
    
    
    # other params ...
);




## Setup of ollama 
system = SystemMessagePromptTemplate.from_template("You are helpful assistant");
humen = HumanMessagePromptTemplate.from_template("{input}")
user_id = "Nkv123"
v_user_id = st.text_input("Please enter user id. example name123","nkv123")
message = [system, MessagesPlaceholder(variable_name='history'),humen]
template = ChatPromptTemplate(messages=message)
chain = template | model | StrOutputParser()

def get_session_history(session_id ):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="sqlite:///chat_history.db"
    )
    
runnable_with_history = RunnableWithMessageHistory(chain,get_session_history,
                                                   input_messages_key='input',
                                                   history_messages_key='history') 

about = '''I am from Moon, And I went on the Sun. I cam here to research about Sun,
How it rotate and about the heat generation''';   


##Streamlit code

st.title("Welcome in ManavEdu Help desk!")
st.write("Please enter you query. I wii assist you with the answer!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


if st.button("Start New Conversation"):
    st.session_state.chat_history = []
    history = get_session_history(user_id)
    # history.clear()

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        


def chat_with_llm(session_id,input):
    # output = runnable_with_history.invoke({'input':input},config={'configurable': {'session_id':session_id}})
    # return output; 
    for output in runnable_with_history.stream({'input':input},config={'configurable':{'session_id':session_id}}):
        
      yield output

        
prompt = st.chat_input("Write your query!")
# st.write(prompt)
    
if prompt:
    st.session_state.chat_history.append({'role':'user','content':prompt})
      
    with st.chat_message('user'):
        st.markdown(prompt)
    
    # response = chat_with_llm(v_user_id,prompt) 
    with st.chat_message('assistant'):
      response=  st.write_stream(chat_with_llm(v_user_id,prompt))
    st.session_state.chat_history.append({'role':'assistant','content':response})