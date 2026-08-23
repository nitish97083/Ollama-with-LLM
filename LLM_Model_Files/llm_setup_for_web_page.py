
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder, SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory


from llm_model import model
from langchain_core.output_parsers import StrOutputParser

system = SystemMessagePromptTemplate.from_template("You are helpful AI assistant who answer user question based on provided context") 
humen = """Answer user question based on provide context ONLY.
If you do not know the answer. Just say, "I do not know the answer".
### Context: {context}
# ### Question: {question}
# ### Answer: """
humen_message = HumanMessagePromptTemplate.from_template(humen)

message = [system,humen_message]

# message = [system,MessagesPlaceholder(variable_name='history'),humen_message]

template = ChatPromptTemplate(message)

qna_chain = template | model | StrOutputParser()
# print(qna_chain)

# u_ques = 'Examine the context and re-write the Profile Summary'

## Below lines are for holding sitory


def get_session_history(session_id ):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="sqlite:///chat_web_history1.db"
    )
    
runnable_with_history = RunnableWithMessageHistory(qna_chain,
                                                   get_session_history,
                                                   input_messages_key='question',
                                                   history_messages_key='history') 

def chat_with_llm(session_id,question,context):
    input_data = {
        'question': question,
        'context': context}
    
    config = {'configurable': {'session_id': session_id}}
    for chunk in runnable_with_history.stream(input_data,config= config):
        
      yield chunk
        # if hasattr(chunk, 'content'):
        #     yield chunk.content
        # elif isinstance(chunk, dict) and 'output' in chunk:
        #     yield chunk['output']
        # else:
        #     yield str(chunk)



def ask_llm(context,question):
  return qna_chain.invoke({'context': context,'question':question})

# my_context = "I am Nitish and my stock share price is 500"
# my_question = "Tell me who am I? and what is  stock share price?"

# response = ask_llm(context=my_context,question=my_question)
# print(response)
# # Call the streaming function
# for token in chat_with_llm("session_abc_123", my_question, my_context):
#     print(token, end="", flush=True)