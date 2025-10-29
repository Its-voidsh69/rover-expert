# 🧠 RAG-Powered Q&A Chatbot

A lightweight **Retrieval-Augmented Generation (RAG)** system built with **Flask**, **LangChain**, and **ChromaDB**, supporting document uploads, semantic search, expert question handling, and text improvement features.  
This project integrates **Anthropic Claude** and **DeepSeek** LLMs for intelligent Q&A and summarization tasks.

---

## 🚀 Features

- **RAG-based Q&A:** Retrieve contextually relevant answers from uploaded documents.  
- **Document Upload & Indexing:** Supports `.txt`, `.pdf`, `.csv`, `.docx`, and `.md`.  
- **Expert Question Handling:** Store and manage user questions in SQLite.  
- **Semantic Search:** Retrieve top relevant chunks from your vector database.  
- **Text Improvement & Summarization:** Use LLMs to polish or summarize text.  
- **LLM Flexibility:** Easily switch between **Anthropic** and **DeepSeek**.  
- **Persistent Vector Store:** Uses **ChromaDB** for long-term embedding storage.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Flask (Python 3.9+) |
| **Vector Database** | [ChromaDB](https://www.trychroma.com/) |
| **LLM Integration** | Anthropic Claude / DeepSeek |
| **Embeddings** | HuggingFace (`all-MiniLM-L6-v2`) |
| **Database** | SQLite |
| **Libraries** | LangChain, Flask-CORS, HuggingFace Embeddings |

---

## ⚙️ Installation and Setup

### 1️⃣ Clone the Repository
```bash

2️⃣ Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Start a ChromaDB Server

Run ChromaDB locally (default port: 8000):

chroma run --host localhost --port 8000

5️⃣ Set Environment Variables

Create a .env file in your project root:

MODEL_PROVIDER=anthropic        # Options: anthropic / deepseek
MODEL_NAME=claude-3-opus-20240229
ANTHROPIC_API_KEY=your_anthropic_key
DEEPSEEK_API_KEY=your_deepseek_key
EMBEDDINGS_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
CHROMA_HOST=localhost
CHROMA_PORT=8000
TARGET_SOURCE_CHUNKS=k

6️⃣ Run the Flask Server
python app.py

🔍 API Endpoints
🧠 1. Query RAG

POST /query

{
  "query": "What is the refund policy?",
  "debug": true
}


Response:

{
  "question": "What is the refund policy?",
  "answer": "Refunds are processed within 5 business days.",
  "sources": [
    {"source": "policy.pdf", "content": "Refunds are processed..."}
  ],
  "time_taken": "1.42 seconds"
}

📄 2. Upload Documents

POST /upload-docs

Upload multiple files as form-data:

files: [file1.pdf, file2.txt]


Response:

{"message": "120 document chunks added to RAG successfully!"}

🧾 3. Add Custom Text

POST /add-to-rag

{
  "title": "Privacy Policy",
  "content": "We value user privacy..."
}


Response:

{"message": "Custom text added successfully!"}

💬 4. Ask an Expert

POST /ask-expert

{
  "question": "What are the nutritional benefits of oats?"
}


Response:

{"message": "Question submitted successfully!"}

📋 5. List All Questions

GET /list-questions?limit=10&offset=0

Response:

{
  "questions": [
    {"id": 1, "question": "What is...", "status": "pending", "timestamp": "2025-10-29 14:10:00"}
  ],
  "count": 1
}

✅ 6. Mark Question as Done

POST /mark-question-done

{
  "question_id": 1
}


Response:

{"message": "Question 1 marked as done!"}

✍️ 7. Improve or Summarize Text

POST /improve-text

{
  "text": "This is an example sentence.",
  "operation": "improve"   // or "summarize"
}


Response:

{
  "original_text": "This is an improved version of your sentence...",
  "operation": "improve"
}

📘 Example Workflow

1️⃣ Upload knowledge documents using /upload-docs
2️⃣ Ask a question using /query
3️⃣ If LLM can’t answer → submit via /ask-expert
4️⃣ Manage questions using /list-questions or /mark-question-done
