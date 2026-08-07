
from llm_model import model;
from langchain_core.output_parsers import CommaSeparatedListOutputParser, JsonOutputParser, NumberedListOutputParser, PydanticOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")
    rating: Optional[int] = Field(default=None, description="The rating of the joke is from 1 to 10, where 1 is the worst and 10 is the best")

#Jon parsor 
   
parser = PydanticOutputParser(pydantic_object=Joke)

instruction = parser.get_format_instructions()
template= '''
    Answer the user query with a joke. Here is the your format instruction. 
    {format_instructions}
    Query = {query}
    Answer: ''';
    
format = PromptTemplate(
    template=template
    ,
    input_variables=["query"],
    partial_variables={'format_instructions': parser.get_format_instructions()},
);
#  This is the standard flow when we use with Prompt Template and PydanticOutputParser.
# chain = format | model | parser;
# try:
#  response = chain.invoke({"query": "Tell me a joke about cat in 1 line in humen readable format."});
#  print(f"Response: {response}");
# except ValidationError as e:
#     print(f"Validation Error: {e.json()}");

#The below code is for JsonOutputParser with Prompt Template.
# j_parser = JsonOutputParser(pydantic_object=Joke)  
# j_instruction = j_parser.get_format_instructions()
# chain = format | model | j_parser
# response = chain.invoke({"query": "Tell me a joke about Lion."});
# print(f"Response: {response}");

#The below code is for String output with structured.    
# structured_llm = model.with_structured_output(Joke);
# response = structured_llm.invoke("Tell me a joke about Lion");
# print(f"Response: {response}");

c_parser = CommaSeparatedListOutputParser();
C_formate_instruction = c_parser.get_format_instructions();
n_parser = NumberedListOutputParser();
n_formate_instruction = n_parser.get_format_instructions();
c_template= '''
    Answer the user query. Here is the your format instruction. 
    {c_formate_instruction}
    Query = {query}
    Answer: ''';
    
format = PromptTemplate(
    template=c_template
    ,
    input_variables=["query"],
    partial_variables={'c_formate_instruction': C_formate_instruction},
);
print(f"Format Instruction: {C_formate_instruction}");
chain = format | model | c_parser;
response = chain.invoke({"query": "generate my website seo keywords. I have contents about NLP and LLM"});
print(f"Response: {response}");

# n_parser = NumberedListOutputParser();
# print(parser.get_format_instructions());
# print(n_parser.get_format_instructions());

