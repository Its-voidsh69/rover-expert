# 🧠 RAG-Powered API with Flask, LangChain, and ChromaDB

A lightweight **Retrieval-Augmented Generation (RAG)** system built with **Flask**, **LangChain**, and **ChromaDB**, supporting document uploads, semantic search, expert question handling, and text improvement features.  
This project integrates **Anthropic Claude** and **DeepSeek** LLMs for intelligent Q&A and summarization tasks.

---

## 🚀 Features

- **RAG-based Q&A**: Retrieve contextually relevant answers from uploaded documents.  
- **Document Upload & Indexing**: Supports `.txt`, `.pdf`, `.csv`, `.docx`, and `.md`.  
- **Expert Question Handling**: Store and manage user questions in SQLite.  
- **Semantic Search**: Retrieve top relevant chunks from your vector database.  
- **Text Improvement & Summarization**: Use LLMs to polish or summarize text.  
- **LLM Flexibility**: Switch easily between **Anthropic** and **DeepSeek**.  
- **Persistent Vector Store**: Uses a ChromaDB instance for embeddings.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Flask (Python 3.9+) |
| Vector Database | [ChromaDB](https://www.trychroma.com/) |
| LLM Integration | Anthropic Claude / DeepSeek |
| Embeddings | HuggingFace (`all-MiniLM-L6-v2`) |
| ORM/Database | SQLite |
| Libraries | LangChain, Flask-CORS, HuggingFace Embeddings |

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/rag-flask-api.git
cd rag-flask-api
2. Create a Virtual Environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate   # (on macOS/Linux)
venv\Scripts\activate      # (on Windows)
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Start a ChromaDB Server
Run a ChromaDB server locally (default port: 8000):

bash
Copy code
chroma run --host localhost --port 8000
5. Set Environment Variables
Create a .env file (or export manually):

bash
Copy code
MODEL_PROVIDER=anthropic        # Options: anthropic / deepseek
MODEL_NAME=claude-3-opus-20240229
ANTHROPIC_API_KEY=your_anthropic_key
DEEPSEEK_API_KEY=your_deepseek_key
EMBEDDINGS_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
COLLECTION_NAME=easyeat_collection
CHROMA_HOST=localhost
CHROMA_PORT=8000
TARGET_SOURCE_CHUNKS=4
6. Run the Server
bash
Copy code
python app.py
Server runs at:

arduino
Copy code
http://localhost:5002
🔍 API Endpoints
🧠 Query RAG
POST /query

json
Copy code
{
  "query": "What is the refund policy?",
  "debug": true
}
Response:

json
Copy code
{
  "question": "What is the refund policy?",
  "answer": "Refunds are processed within 5 business days.",
  "sources": [{"source": "policy.pdf", "content": "Refunds are processed..."}],
  "time_taken": "1.42 seconds"
}
📄 Upload Documents
POST /upload-docs
Upload multiple files (multipart form):

makefile
Copy code
files: [file1.pdf, file2.txt]
Response:

json
Copy code
{"message": "120 document chunks added to RAG successfully!"}
🧾 Add Custom Text
POST /add-to-rag

json
Copy code
{
  "title": "Privacy Policy",
  "content": "We value user privacy..."
}
💬 Ask an Expert
POST /ask-expert

json
Copy code
{
  "question": "What are the nutritional benefits of oats?"
}
Response:

json
Copy code
{"message": "Question submitted successfully!"}
📋 List All Questions
GET /list-questions?limit=10&offset=0

json
Copy code
{
  "questions": [
    {"id": 1, "question": "What is...", "status": "pending", "timestamp": "2025-10-29 14:10:00"}
  ],
  "count": 1
}
✅ Mark Question as Done
POST /mark-question-done

json
Copy code
{
  "question_id": 1
}
Response:

json
Copy code
{"message": "Question 1 marked as done!"}
🔍 Debug Retrieval
POST /debug-retrieve

json
Copy code
{
  "query": "What are antioxidants?"
}
Returns the most relevant chunks from the Chroma collection.

✍️ Improve or Summarize Text
POST /improve-text

json
Copy code
{
  "text": "This is an example sentence.",
  "operation": "improve"   // or "summarize"
}
Response:

json
Copy code
{
  "original_text": "This is an improved version of your sentence...",
  "operation": "improve"
}
🏥 Health Check
GET /

json
Copy code
{
  "status": "RAG API connected to Chroma!",
  "host": "localhost",
  "port": 8000,
  "collection": "easyeat_collection"
}
🧱 Database Schema (SQLite)
Table: expert_questions

Column	Type	Description
id	INTEGER	Primary key
question	TEXT	User question
status	TEXT	Default 'pending'
timestamp	DATETIME	Auto timestamp

📘 Example Workflow
Upload knowledge documents via /upload-docs.

Ask a question using /query.

If LLM can’t answer → submit to /ask-expert.

Manage expert questions using /list-questions.

💡 Notes
Designed for local RAG assistants and small-scale knowledge apps.

Ensure the Chroma server is running before Flask starts.

For production, persist Chroma data and enable authentication
