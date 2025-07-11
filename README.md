# BrainlyBot — Context-Aware AI Tutor with RAG

**BrainlyBot** is a smart educational assistant powered by Azure OpenAI and Azure Cognitive Search. It helps students get instant, accurate answers grounded in real institutional study materials — turning generic AI into a personalized tutor.

## Overview

BrainlyBot answers academic and technical queries using your organization's knowledge base (PDFs, notes, documents, etc.). It leverages **Azure Blob Storage** to store materials, **OpenAI embeddings** to vectorize content, and **Azure Cognitive Search** to retrieve relevant chunks. GPT-4o then crafts context-rich, step-by-step explanations using **RAG (Retrieval-Augmented Generation)**.


## Features
1. AI Tutor for academic and technical subjects
2. Personalized learning based on your own organization’s study materials
3. Retrieval-Augmented Generation (RAG) using Azure Cognitive Search
4. Powered by GPT-4o through Azure OpenAI for accurate, step-by-step responses
5. Student-friendly web interface with a clean and responsive design
6. FastAPI backend integrated with LangChain for orchestration
7. Support for various file types (PDF, DOCX, etc.) to embed and index study material
8. Secure environment configuration using .env for all secrets and keys


##  Tech Stack

| Layer       | Technology                     |
|-------------|---------------------------------|
| **Frontend**| HTML, CSS, JavaScript           |
| **Backend** | FastAPI, LangChain              |
| **AI Model**| GPT-4o via Azure OpenAI         |
| **Search**  | Azure Cognitive Search          |
| **Storage** | Azure Blob Storage              |
| **Embedding**| Azure OpenAI Embedding Models |
| **Security**| Python dotenv for config        |



## ⚙️Set up 



```bash
1. Clone the repository

git clone https://github.com/rambajpai19/brainlybot.git
cd ContextBasedConversationalChatbot

2. Set up the backend

cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

#Install dependencies
pip install -r requirements.txt
uvicorn main:app --reload


3. Configure environment Create a .env file in the root directory:

OPENAI_API_KEY=your_openai_key
AZURE_ENDPOINT=https://your-openai-resource.openai.azure.com/
DEPLOYMENT_NAME=gpt-4o-team01
MODEL_NAME=gpt-4o

SEARCH_ENDPOINT=https://your-search.search.windows.net/
SEARCH_KEY=your_search_key
INDEX_NAME=your_index_name

4. Launch the frontend
/frontend/index.html


##Project Structure

📁 ContextBasedConversationalChatbot/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env              
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
├── README.md


#Use Cases
1. Internal knowledge base Q&A for educational institutions
2. Student help desk for subject-based queries
3. Personalized academic assistant for self-paced learning
4. Querying internal documentation or SOPs
