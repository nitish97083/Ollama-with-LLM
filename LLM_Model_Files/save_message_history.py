from llm_model  import model;
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage

template = ChatPromptTemplate.from_template("Context: {context}\n\n Question: {question}")


chain = template | model | StrOutputParser()

# about = "I am a Kant, student of ManavEdu School. I am learning ollama model with LLM";

# prompt = "Tell me who am i?";

#below code are to get session history only
# response = chain.invoke({
#     "context": about,
#     "question": prompt
# })
# print(f" response is --> {response}");    




# CHANGED: We now use a single file to keep track of the growing conversation history
HISTORY_FILE = "chat_history.txt"

# 2. AUTOMATIC LOADING (Checks if you ran this before)
if os.path.exists(HISTORY_FILE):
    print("--- Loaded from past history ---")
    # CHANGED: Load the entire saved history to use as your context
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        about = f.read()
    
    # NEW: Ask a new follow-up question for your next chat turn
    prompt = "Do you know what we discussed till now?" 
else:
    print("--- First time setup: Saving your inputs ---")
    # Your exact starting inputs
    about = "I am a Kant, student of ManavEdu School. I am learning ollama model with LLM"
    prompt = "what is my name and what am i doing in ManavEdu School?"
    
    # CHANGED: Save the initial background into the history file to start the chain
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write(about)

# 3. YOUR EXACT CHAIN INVOCATION
response = chain.invoke({
    "context": about,
    "question": prompt
})

print(f"\nresponse is --> {response}")

# =====================================================================
# NEW: APPEND THE NEW CHAT TURN TO THE FILE
# =====================================================================
# Using "a" mode adds the new text to the bottom of the file without overwriting it
with open(HISTORY_FILE, "a", encoding="utf-8") as f:
    f.write(f"\n\nQuestion: {prompt}")
    f.write(f"\nResponse: {response}")
print("\n--- New chat successfully added to history file! ---")

