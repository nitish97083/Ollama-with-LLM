
import os


from langchain_core.messages import HumanMessage
from llm_model import model
from langchain_core.tools import tool
from langchain_tavily import TavilySearch




# api_key = os.getenv("API_KEY")



@tool
def add(a,b):
    """
    Add two integer number
    args:
     a: First integer
     b: Second Integer 
    """
    return a+b;

@tool
def multiply(a:int,b:int )->int: 
    """
    Multiply two integer number
    args:
     a: First integer
     b: Second Integer 
    """
    return int(a)*int(b)

# print(add.args_schema.schema())




# res = llm_with_tools.invoke(question).tool_calls
# print(f"Resoponse is {res}")

# Tavily search *******************************************
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")
# print(f"end_point: {api_key}")

@tool
def tavily_search(query):
   """ Search the web for the real time and latest news.
    for  example, Stock price, news, weather update etc.
    
    Args:
    query: The search query
    """
   search = TavilySearch(
    max_results=1,
    topic="general",
    include_answer=True,
    include_raw_content=True,
    # include_images=False,
    # include_image_descriptions=False,
    search_depth="advanced",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
   )
   response = search.invoke(query)
   return response





#  Code to integrate with Wikipedia *****************************

from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
import wikipedia

@tool
def wiki_search(query):
    
    """  Search wikipedia for general information.
         for example, Capital of India, etc.
        
        Args:
        query: The search query
        """
    # Set user so that Wikipedia do not block the  request
    wikipedia.set_user_agent("my-langchain-app/1.0 (contact@example.com)")

    # Initialize the wrapper (fetches summaries by default)
    # wikipedia1 = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1000)
    wikipedia2 = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    docs = wikipedia2.run(query)
    return docs

wi_q = "What is the capital of India"
q_mu = 'what will be 5 into 10'
q_add = 'Add 20 and 30. Also multiply them'
t_q = "tell me latest stock price of TCS"
# Design LLM and create runnable to execute the tools

tools = [tavily_search,wiki_search,multiply,add]

list_of_tools = {tool_name.name: tool_name for tool_name in tools }
# print(list_of_tools)
v_messages = [HumanMessage(wi_q)]
# print(f" v-massage = {v_messages}")
llm_with_tools = model.bind_tools(tools)

ai_message = llm_with_tools.invoke(v_messages)

for tool_call in ai_message.tool_calls:
    print(f"The name of tool call is {tool_call['name']} \n")
    name  = tool_call["name"].lower()
    
    selected_tool = list_of_tools[name]
    # print(f" selected_tool is {selected_tool}")
    tool_msg = selected_tool.invoke(tool_call)
    v_messages.append(tool_msg)
    
    
for chunk in llm_with_tools.stream(v_messages):
    print(chunk.content,end="", flush=True)    

    





