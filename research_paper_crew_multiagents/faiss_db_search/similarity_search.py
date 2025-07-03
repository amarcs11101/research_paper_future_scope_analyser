import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

VECTOR_DB_DIR = "./vector_db"
INDEX_FILE_PATH = os.path.join(VECTOR_DB_DIR, "index.faiss")

def get_embeddings():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("Missing OPENAI_API_KEY in environment.")
    
    return OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small"),
        openai_api_key=openai_api_key
    )

def search_vector_db(query: str):
    embeddings = get_embeddings()

    if not os.path.exists(INDEX_FILE_PATH):
        print("No vector DB found. Returning empty result.")
        return []

    try:
        db = FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)
        print("Vector DB loaded.")
        results = db.similarity_search(query, k=3)
        return results
    except Exception as e:
        print(f"[!] Failed to load or search vector DB: {e}")
        return []

def save(query: str, result: str):
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    print("### Saving new record in vector DB ###")

    embeddings = get_embeddings()
    combined = f"Q: {query}\nA: {result}"

    # Chunk the data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.create_documents([combined])
    print("### Chunked the data ###")

    try:
        if os.path.exists(INDEX_FILE_PATH):
            db = FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)
            print("Vector DB loaded. Adding new chunks.")
            db.add_documents(chunks)
        else:
            raise FileNotFoundError("Vector DB not found. Creating new one.")
    except Exception as e:
        print(f"[!] {e}")
        print("Creating new FAISS DB from documents.")
        db = FAISS.from_documents(chunks, embeddings)

    db.save_local(VECTOR_DB_DIR)
    print("########## Data saved to vector DB ##########")
