from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv
import os

load_dotenv()


class QdrantRetriever:
    def _init__(self, collection_name: str):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_HOST"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = "qdrant-openai-docs"

        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=1536,  # Tamaño del vector de embeddings
                distance=Distance.COSINE  # Tipo de distancia   
            )
        )
        self.model = "text-embedding-ada-002"

    
    def retrieve(self, query: str, limit: int = 10):
        """Retrieve documents from Qdrant based on a query."""
        response = self.client.search(
            collection_name=self.collection_name,
            query=query,
            limit=limit
        )
        concatenated_content = "\n\n\n --- \n\n\n".join([
    hit.payload.get("text", "") for hit in response
])
        return concatenated_content