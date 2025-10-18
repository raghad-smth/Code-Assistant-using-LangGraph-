import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# loading the API key 
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# function that takes the model name and return the llm object 
def get_llm(model_name): 
    llm = ChatOpenAI(
    model=model_name,
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    temperature=0.0
    )
    return llm 

# loading the dataset 
from datasets import load_dataset
dataset = load_dataset("openai/openai_humaneval", split="test")
df = dataset.to_pandas()

# Creaing only a subset for the needed columns 
subset = df[["task_id", "prompt", "canonical_solution"]]
subset.columns
print(subset.head())