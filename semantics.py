from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document



def semantic_summary(posts):
    documents = [Document(page_content=post["text"], metadata={"image": post["image"]}) for post in posts]
    embedding_model = OpenAIEmbeddings()
    index = FAISS.from_documents(documents, embedding_model)
    query = "Reports of a strange or unidentified drone spotted near the front line"
    results = index.similarity_search(query, k=)  # top 10 semantically similar chunks
