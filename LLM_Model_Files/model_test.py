

# import os
# from dotenv import load_dotenv

# load_dotenv()

# print("Tracing Active:", os.getenv("LANGSMITH_TRACING_V2"))
# print("Target Project:", os.getenv("LANGSMITH_PROJECT"))

# Above line to invoke with LangSmith for debug.

from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,SystemMessage; # This is to pass the Role and 
#user Message to get bettter answer.
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    ChatMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
    );

from llm_model import model;
# response = model.invoke("Hi how are you ");
question = HumanMessagePromptTemplate.from_template("Tell me about the {UserQuery} step by step in {method}?");
role = SystemMessagePromptTemplate.from_template("You are a AI assitant for {Role} admission help desk."
    );
s_role = role.format(Role="ManavEdu School");
h_query = question.format(UserQuery="Admission process",method="short and consize");

# h_ques = HumanMessage(content=question);
# sys_msg = SystemMessage(content=role);
# print(f"Human Message: {h_ques} and System Message: {sys_msg}");



messages = [h_query, s_role];
template = ChatPromptTemplate(messages=messages);


'''below code is  standard flow when we use with Template Prompt'''
#m_ques = template.invoke({"UserQuery":"Admission process","method":"short and consize","Role":"ManavEdu Hospital"});
# print(f" messages : {messages} -->  ");
# print();
# print(f"template : {template}")
# print();
# print(f" and Message: {m_ques}")
# for chunk in model.stream(m_ques):
#     print(chunk.content, end="", flush=True)
# print()

'''***********************Comments'''

#these are for chain code where Pipe operator is used to invoke the model with prompt template.
args = {"UserQuery":"Admission process","method":"short and consize","Role":"ManavEdu School"};
chain = template | model |StrOutputParser();
# response = chain.invoke(args);
#print(f"Response: {response}");

#**********************
#This below line is for streaming the response from the model with prompt template.
# for chunk in chain.stream(args):
#     print(chunk, end="", flush=True)
# print()  ***********************


#These below line are to get analyzed response from model response using analysis prompt template and pipe operator.
analysis_promt = ChatPromptTemplate.from_template('''Analyze the response {response} and provide 
a summary of the key points, highlighting any important details or recommendations in 3 lines.
Response should be in humen readabale format  ''');

# fact_check_promt = analysis_promt | model | StrOutputParser();
# analysis_response = fact_check_promt.invoke({"response":response});

'''This below lines are for composed chain. Where we created a chain with chain 
line 72 response '''
composed_chain = {"response": chain}|analysis_promt |model | StrOutputParser();
analysis_response = composed_chain.invoke({"response":args});
for chunk in composed_chain.stream({"response":args}):
    print(chunk, end="", flush=True)
# print(f"Analysis Response: {analysis_response}");

