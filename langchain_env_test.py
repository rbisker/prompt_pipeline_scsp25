import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# ✅ Test PyTorch
try:
    import torch
    print(f"[✔] PyTorch imported successfully — version: {torch.__version__}")
    
    # Check if CUDA (GPU) is available
    if torch.cuda.is_available():
        print(f"[✔] CUDA is available — GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("[ℹ] CUDA not available — running on CPU only")

except ImportError as e:
    print("[✖] PyTorch is not installed")


# ✅ Test OpenAI Chat
try:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    print("[✔] langchain_openai ChatOpenAI is working")
except Exception as e:
    print("[✖] Error with langchain_openai ChatOpenAI:", e)

# ✅ Text splitting
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    print("[✔] Text splitter is working")
except Exception as e:
    print("[✖] Error with text splitting:", e)

# ✅ FAISS + OpenAI Embeddings
try:
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    # from langchain_huggingface import HuggingFaceEmbeddings
    from langchain.docstore.document import Document

    docs = [Document(page_content="Test document")]
    db = FAISS.from_documents(docs, OpenAIEmbeddings())
    print("[✔] FAISS vector store is working")
except Exception as e:
    print("[✖] Error with FAISS or embeddings:", e)

# ✅ tiktoken
try:
    import tiktoken
    enc = tiktoken.encoding_for_model("gpt-4o")
    print(f"[✔] tiktoken loaded ({enc.name})")
except Exception as e:
    print("[✖] Error with tiktoken:", e)
