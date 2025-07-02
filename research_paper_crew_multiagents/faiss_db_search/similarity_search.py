import os 
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings 
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
VECTOR_DB_DIR = "./vector_db"
load_dotenv()

def search_vector_db(query: str):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small"))

    try:
        db = FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)
        print(" Vector DB loaded.")
    except Exception:
        print(" No vector DB found. Returning empty result.")
        return []
 
    results = db.similarity_search(query, k=3)
    return results


def save(query: str, result: str):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings()
    combined = f"Q: {query}\nA: {result}" 

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  
        chunk_overlap=50
    )
    chunks = text_splitter.create_documents([combined])
    try:
        db = FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)
        print("Vector DB loaded for saving.")
    except Exception as e:
        print(e)
        print("No existing vector DB. Creating new one.")
        db = FAISS.from_documents(chunks, embeddings)
    else:
        db.add_documents(chunks)

    db.save_local(VECTOR_DB_DIR)
    print("Data saved to vector DB.")

