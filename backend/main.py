from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableMap
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import QueryType
from dotenv import load_dotenv
import os

# === Configuration ===
load_dotenv()  

OPENAI_API_KEY  = os.getenv("AZURE_OPENAI_KEY")  
AZURE_ENDPOINT =  os.getenv("AZURE_OPENAI_ENDPOINT") 
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
MODEL_NAME = os.getenv("MODEL_NAME")
SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("SEARCH_KEY")    
INDEX_NAME = os.getenv("INDEX_NAME")


# System Prompt 
SYSTEM_PROMPT = """
You are an expert teacher with deep knowledge across all academic and technical subjects.
For simple questions, provide a brief, accurate answer (1-2 sentences).
For complex questions or when the user requests explanation, give clear, step-by-step explanations with examples.
"""

# App Setup 
app = FastAPI()

# Enable CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Input/Output Models 
class ChatRequest(BaseModel):
    input: str

class ChatResponse(BaseModel):
    response: str
    tokens_used: int

# Azure OpenAI Setup 
llm = AzureChatOpenAI(
    openai_api_version="2025-01-01-preview",
    temperature=0.5,
    max_tokens=2000,
    azure_deployment=DEPLOYMENT_NAME,
    azure_endpoint=AZURE_ENDPOINT,
    openai_api_key=OPENAI_API_KEY,
)

# Azure Search Setup 
search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_KEY)
)

# Context Retrieval from Azure Search
def get_context_from_search(user_prompt: str) -> str:
    try:
        results = search_client.search(
            search_text=user_prompt,
            select="chunk,title",
            query_type=QueryType.SIMPLE,
            semantic_configuration_name="semantictest-semantic-configuration",
        )
        chunks = [r["chunk"] for r in results if r.get("chunk")]
        return "\n".join(chunks[:20])
       
    except Exception as e:
        return f"Error fetching search results: {str(e)}"

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("Relevant document context:\n{context}\n\nStudent: {input}")
])

# In-Memory Chat History 
class MyChatHistory:
    def __init__(self):
        self.messages: List[BaseMessage] = []

    def add_user_message(self, text: str):
        self.messages.append(HumanMessage(content=text))

    def add_ai_message(self, text: str):
        self.messages.append(AIMessage(content=text))

store = {}

def get_memory(session_id: str) -> MyChatHistory:
    if session_id not in store:
        store[session_id] = MyChatHistory()
    return store[session_id]

# LangChain Chat Chain 
base_chain = RunnableMap({
    "input": lambda x: x["input"],
    "context": lambda x: get_context_from_search(x["input"]),
    "history": lambda x: get_memory(x["session_id"]).messages
}) | prompt | llm

chatbot = RunnableWithMessageHistory(
    base_chain,
    get_memory,
    input_messages_key="input",
    history_messages_key="history"
)

# POST Endpoint 
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = "default-session"
    with get_openai_callback() as cb:
        result = chatbot.invoke(
            {"input": request.input, "session_id": session_id},
            config={"configurable": {"session_id": session_id}}
        )
        store[session_id].add_user_message(request.input)
        store[session_id].add_ai_message(result.content)
        return ChatResponse(response=result.content, tokens_used=cb.total_tokens)

@app.get("/chat", response_model=ChatResponse)
async def chat_get(input: str = Query(..., description="The user's query")):
    session_id = "default-session"
    with get_openai_callback() as cb:
        result = chatbot.invoke(
            {"input": input, "session_id": session_id},
            config={"configurable": {"session_id": session_id}}
        )
        store[session_id].add_user_message(input)
        store[session_id].add_ai_message(result.content)
        return ChatResponse(response=result.content, tokens_used=cb.total_tokens)

# Optional Root Endpoint 
@app.get("/")
def read_root():
    return {"message": "Azure AI Chatbot is running "}
