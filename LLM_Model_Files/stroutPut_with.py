from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import Optional
from llm_model import model

# 1. Define your schema
class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")
    rating: Optional[int] = Field(default=None, description="Rating from 1 to 10")

# 2. Force Ollama into JSON mode
# llm = ChatOllama(
#     model="llama3",       # Or your specific model
#     temperature=0,        # Lower temperature prevents structure drifting
#     format="json"         # CRITICAL: This stops it from returning the raw schema map
# )

# 3. Bind the schema directly to the model
structured_llm = model.with_structured_output(Joke)
  


# 4. Invoke the chain directly
response = structured_llm.invoke("Tell me a funny joke about a cat")
print(response)

#this is  for 

