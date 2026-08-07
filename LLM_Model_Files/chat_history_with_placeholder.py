from llm_model import model

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage,SystemMessage


system = SystemMessagePromptTemplate.from_template("You are helpful assistant");
humen = HumanMessagePromptTemplate.from_template("{input}")

message = [system,MessagesPlaceholder(variable_name="history"),humen]

template = ChatPromptTemplate(messages=message)

chain = template | model | StrOutputParser()

def get_session_history(session_id):
 return SQLChatMessageHistory(
    session_id=session_id, 
    connection="sqlite:///chat_history.db")
 
runnable_with_history = RunnableWithMessageHistory(chain,get_session_history,
                                                   input_messages_key= 'input',
                                                   history_messages_key='history'
                                                   ) 

about = '''I am from Moon, And I went on the Sun. I cam here to research about Sun,
How it rotate and about the heat generation''';

def chat_with_llm(session_id,input):
    output = runnable_with_history.invoke(
        {'input':input},
        config={'configurable': {'session_id':session_id}}
    )
    return output; 

user_id = 'Test123'
response = chat_with_llm(user_id,"JTell me who am I?")
print(f"response --> {response}")
