import chromadb
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama

def read_pdf_and_split(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    all_text = "\n".join(doc.page_content for doc in documents)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(all_text)
    return chunks

def vectorize_text(text_chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    vectors = model.encode(text_chunks)
    return vectors, model

def create_chroma_index(vectors, text_chunks, persist_directory):
    client = chromadb.PersistentClient(path=persist_directory)
    db = client.get_or_create_collection(name="pdf_collection")
    db.add(documents=text_chunks, embeddings=vectors)
    return db

def query_chroma(query, model, db, k=3):
    query_vector = model.encode([query])
    results = db.query(query_embeddings=query_vector, n_results=k)
    retrieved_chunks = [doc for doc in results['documents'][0]]
    return retrieved_chunks

def send_to_ollama(retrieved_chunks):
    input_text = " ".join(retrieved_chunks)
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": input_text}])
    return response['message']['content']


if __name__ == "__main__":
    pdf_path = "CUDA_C_Programming_Guide.pdf"
    query = "What is the summary of the document?"
    persist_directory = "./chroma_storage"
    text_chunks = read_pdf_and_split(pdf_path)

    vectors, model = vectorize_text(text_chunks)

    db = create_chroma_index(vectors, text_chunks, persist_directory)

    retrieved_chunks = query_chroma(query, model, db)

    generated_text = send_to_ollama(retrieved_chunks)
    print(generated_text)