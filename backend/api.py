#!/usr/bin/env python3
import os
import time
import sqlite3
import chromadb
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, Docx2txtLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# ✅ Environment Variables
#MODEL = os.getenv("MODEL", "mistral")
MODEL = os.getenv("MODEL", "claude-3-opus-20240229")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
TARGET_SOURCE_CHUNKS = int(os.getenv("TARGET_SOURCE_CHUNKS", 4))

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "easyeat_collection")

DB_FILE = "expert_questions.db"

LOADER_MAPPING = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".docx": Docx2txtLoader,
    ".md": UnstructuredMarkdownLoader,
}

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)

# ✅ SQLite Database Initialization
def init_db():
    """Initialize SQLite database to store expert questions"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expert_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                status TEXT DEFAULT 'pending',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# ✅ Chroma Initialization
print(f"🔌 Connecting to Chroma server at {CHROMA_HOST}:{CHROMA_PORT}...")

# ✅ Initialize ChromaDB Client
chroma_client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT
)

# ✅ Initialize Embeddings
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)

# ✅ Connect to the Running Chroma Server
print(f"🔌 Connecting to Chroma server at {CHROMA_HOST}:{CHROMA_PORT}...")
vectorstore = Chroma(
    client=chroma_client,
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": TARGET_SOURCE_CHUNKS})
#llm = OllamaLLM(model=MODEL)
llm = ChatAnthropic(model=MODEL, anthropic_api_key=ANTHROPIC_API_KEY)


qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)
print("🚀 RAG system connected to Chroma server!")

# ✅ Utility Functions
def perform_semantic_search(query, k=TARGET_SOURCE_CHUNKS):
    """ Perform semantic search without generating an answer """
    try:
        docs = retriever.get_relevant_documents(query)
        sources = [{"source": doc.metadata.get("source", "Unknown"), "content": doc.page_content} for doc in docs]
        return sources
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return []

def execute_query(query, params=()):
    """Execute SQLite query with error handling"""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()
    except Exception as e:
        print(f"DB Error: {e}")
        return []

# ✅ Routes
@app.route('/query', methods=['POST'])
def query():
    """ Query the RAG system """
    try:
        data = request.get_json()
        query = data.get("query", "")
        semantic_only = data.get("semantic_only", False)

        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400

        start = time.time()
        
        if semantic_only:
            sources = perform_semantic_search(query)
            response = {
                "question": query,
                "sources": sources,
                "time_taken": f"{time.time() - start:.2f} seconds"
            }
        else:
            res = qa_chain(query)
            answer = res['result']
            docs = res.get('source_documents', [])
            
            sources = [{"source": doc.metadata.get("source", "Unknown"), "content": doc.page_content} for doc in docs]

            response = {
                "question": query,
                "answer": answer,
                "sources": sources,
                "time_taken": f"{time.time() - start:.2f} seconds"
            }
        
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask-expert', methods=['POST'])
def ask_expert():
    """ Store a question in SQLite DB """
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400

        execute_query("INSERT INTO expert_questions (question) VALUES (?)", (question,))
        
        print(f"📩 New Expert Question: {question}")
        return jsonify({"message": "Question submitted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/upload-docs', methods=['POST'])
def upload_docs():
    """ Upload and index multiple documents into RAG """
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400

        files = request.files.getlist('files')
        all_docs = []

        for file in files:
            if file.filename == '':
                continue

            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in LOADER_MAPPING:
                return jsonify({"error": f"Unsupported file type: {ext}"}), 400

            # Save the uploaded file temporarily
            temp_file_path = f"/tmp/{file.filename}"
            file.save(temp_file_path)

            try:
                # Load and split the document
                loader = LOADER_MAPPING[ext](temp_file_path)
                documents = loader.load()

                # Split documents into smaller chunks
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                docs = text_splitter.split_documents(documents)

                all_docs.extend(docs)
            except Exception as e:
                os.remove(temp_file_path)
                return jsonify({"error": f"Failed to load {file.filename}: {str(e)}"}), 500

            # Clean up temp file
            os.remove(temp_file_path)

        # ✅ Add documents to Chroma
        if all_docs:
            vectorstore.add_documents(all_docs)
            return jsonify({
                "message": f"{len(all_docs)} document chunks added to RAG successfully!"
            }), 200
        else:
            return jsonify({"error": "No valid documents found"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add-to-rag', methods=['POST'])
def add_to_rag():
    """ Add text to the Chroma RAG system """
    try:
        data = request.get_json()
        title = data.get("title", "Untitled Document")
        content = data.get("content", "")

        if not content:
            return jsonify({"error": "Content cannot be empty"}), 400

        # Add the text to the RAG vector store
        vectorstore.add_texts(
            texts=[f"{title}\n{content}"],
            metadatas=[{"source": title}]
        )

        return jsonify({
            "message": f"Text '{title}' added to RAG successfully!"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/list-questions', methods=['GET'])
def list_questions():
    """ Retrieve list of questions from SQLite DB """
    try:
        limit = int(request.args.get("limit", 20))
        offset = int(request.args.get("offset", 0))

        rows = execute_query(
            "SELECT id, question, status, timestamp FROM expert_questions ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )

        questions = [
            {"id": row[0], "question": row[1], "status": row[2], "timestamp": row[3]}
            for row in rows
        ]

        return jsonify({"questions": questions, "count": len(questions)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/question/<int:question_id>', methods=['GET'])
def get_question_by_id(question_id):
    """ Retrieve a specific question by ID """
    try:
        rows = execute_query(
            "SELECT id, question, status, timestamp FROM expert_questions WHERE id = ?",
            (question_id,)
        )

        if not rows:
            return jsonify({"error": "Question not found"}), 404

        question = {
            "id": rows[0][0],
            "question": rows[0][1],
            "status": rows[0][2],
            "timestamp": rows[0][3]
        }

        return jsonify(question), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/mark-question-done', methods=['POST'])
def mark_question_done():
    """ Mark question as done """
    try:
        data = request.get_json()
        question_id = data.get("question_id")

        if not question_id:
            return jsonify({"error": "Question ID is required"}), 400

        execute_query("UPDATE expert_questions SET status = 'done' WHERE id = ?", (question_id,))
        return jsonify({"message": f"Question {question_id} marked as done!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/improve-text', methods=['POST'])
def improve_text():
    """ Improve or summarize text using LLM """
    try:
        data = request.get_json()
        text = data.get("text", "")
        operation = data.get("operation", "improve")

        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400

        prompt = (
            f"Summarize the following text:\n{text}\nSummary:"
            if operation == "summarize"
            else f"Improve the following text:\n{text}\nImproved version:"
        )

        result = llm(prompt)
        # Handle string or dict response
        improved_text = result if isinstance(result, str) else result.get("text", "")

        return jsonify({
            "original_text": improved_text,
            "operation": operation,
            "improved_text": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    """ Health check """
    return jsonify({
        "status": "RAG API connected to Chroma!",
        "host": CHROMA_HOST,
        "port": CHROMA_PORT,
        "collection": COLLECTION_NAME
    }), 200

# ✅ Initialize DB and Start Server
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)
