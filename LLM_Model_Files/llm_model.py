from langchain_ollama import ChatOllama


base_url = "http://localhost:11434";
model = "ManavEdu";
g_model = "gemma4"
llm = "llama3.2"


model = ChatOllama(
    base_url=base_url,
    model=llm,
    #validate_model_on_init=True,
    temperature=0.8,
    num_predict=512,
    num_ctx=512,
    top_k=20,
    top_p=0.2
    
    
    # other params ...
);