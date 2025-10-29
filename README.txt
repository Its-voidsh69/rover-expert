# 🧠 RAG-Powered API with Flask, LangChain, and ChromaDB

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
