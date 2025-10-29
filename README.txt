# 🧠 RAG-Powered Q&A Chatbot

A lightweight **Retrieval-Augmented Generation (RAG)** system built with **Flask**, **LangChain**, and **ChromaDB**, supporting document uploads, semantic search, expert question handling, and text improvement features.  
This project integrates **Anthropic Claude** and **DeepSeek** LLMs for intelligent Q&A and summarization tasks.

---

## 🚀 Features

- **RAG-based Q&A**: Retrieve contextually relevant answers from uploaded documents.
- **Document Upload & Indexing**: Supports `.txt`, `.pdf`, `.csv`, `.docx`, and `.md`.
- **Expert Question Handling**: Stores and tracks user-submitted questions in SQLite.
- **Semantic Search**: Retrieve top relevant chunks from your vector database.
- **Text Improvement & Summarization**: Enhance or summarize text using LLMs.
- **LLM Flexibility**: Switch easily between **Anthropic** and **DeepSeek** models.
- **Persistent Vector Store**: Uses a ChromaDB instance for vector embeddings.

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
