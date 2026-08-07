

from urllib import response

from llm_model import model;
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage,SystemMessage; 
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    ChatMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
    );

user_promt = '''Given the user review below, classify the review as either 'Positive' or 'Negative'.
Do not respond in more than 1 word.
Review: {review}
Classification: ''';

user_prompt_template = ChatPromptTemplate.from_template(user_promt);
chain = user_prompt_template | model| StrOutputParser();
neg_review = "The help desk response is worst rated and I am disappointed!";
pos_review = "The help desk response is very good and I am happy with the service!";



# print(f"Response: {chain.invoke({'review': neg_review})}");
# print(f"Response: {chain.invoke({'review': pos_review})}");

pos_prompt_respose = '''Act as a Patient Relations Specialist for ManavEdu Hospital.
Your task is to draft a highly professional, neutral, and empathetic response like an email
to a positive review in 3 lines.
Review: {review}
'''
neg_prompt_respose = '''Act as a Patient Relations Specialist for ManavEdu Hospital.
Your task is to draft a highly professional, neutral, and empathetic response to a negative review in 3 lines.
and request the user to share the details of the issue on email at test12@gmail.co to resolve the issue.
Review: {review}
'''
pos_prompt_template = ChatPromptTemplate.from_template(pos_prompt_respose);
neg_prompt_template = ChatPromptTemplate.from_template(neg_prompt_respose);

positive_chain = pos_prompt_template | model| StrOutputParser();
negative_chain = neg_prompt_template | model| StrOutputParser();

def route_review(info):
    if 'positive' in info['sentiment'].lower():
        return positive_chain;
    else:
        return negative_chain;

full_chain = {'sentiment': chain,
               'review':lambda x: x['review']
            #  'review':lambda x: (print(f"\n ACTUAL LAMBDA INPUT (x): {x}\n"), x)
} |RunnableLambda(route_review);

# full_chain.invoke({'review': pos_review});
for chunk in full_chain.stream({'review':neg_review}):
     print(chunk, end="", flush=True)
    