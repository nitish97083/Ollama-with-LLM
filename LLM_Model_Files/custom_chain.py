from llm_model import model;
from langchain_core.runnables import chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate



system_role = SystemMessagePromptTemplate.from_template("You are a {school} teacher.You answer in short sentences and in simple words");
  
fact_ques = HumanMessagePromptTemplate.from_template("Tell me the fact about the {topics} in {points} points");

poem_ques= HumanMessagePromptTemplate.from_template("Write a poem on {topics} in {sentences} sentences");
fact_messages = [system_role, fact_ques];
poem_messages = [system_role, poem_ques];


template = ChatPromptTemplate(messages=fact_messages);
fact_chain = template | model | StrOutputParser();
template = ChatPromptTemplate(messages=poem_messages);
poem_chain = template | model | StrOutputParser();

params = {"school":"Primary","topics":"Earth","sentences":3,"points":3};
# for chunk in fact_chain.stream(params):
#     print(chunk, end="", flush=True)


@chain
def custom_chain(params):
    # Define your custom chain logic here
    # For example, you can process the input_data and invoke the model
    return {
           'fact': fact_chain.invoke(params),
           'poem': poem_chain.invoke(params)
         }

output = custom_chain.invoke(params)
print("\n\nFact: ", output['fact']);  
print("\n\nPoem:\n", output['poem']);