from langchain_community.document_loaders import PyMuPDFLoader
from qdrant_client import QdrantClient, models
from langchain_core.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Cargar PDF
loader = PyMuPDFLoader("/ruta/a/nextjs-docs.pdf")
docs = loader.load()

# Embeddings
embeddings = OpenAIEmbeddings()

# Vectorizar y subir a Qdrant
qdrant = QdrantClient(
    url=os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY")
)

qdrant.recreate_collection(
    collection_name="nextjs-pdf",
    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
)

qdrant.upload_collection(
    collection_name="nextjs-pdf",
    vectors=[embeddings.embed_query(doc.page_content) for doc in docs],
    payload=[{"text": doc.page_content} for doc in docs],
    ids=[i for i in range(len(docs))]
)