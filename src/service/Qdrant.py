from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv
import os
import openai

load_dotenv()


class QdrantRetriever:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_HOST"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = "qdrant-openai-docs"

        self.client.recreate_collection(
            collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
            vectors_config=VectorParams(
                size=1536,  # Tamaño del vector de embeddings
                distance=Distance.COSINE  # Tipo de distancia   
            )
        )
        self.model = "text-embedding-ada-002"
    def get_embedding(self, text: str):
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.embeddings.create(
                input=[text],
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error al generar embedding: {e}")
            return None
    def retrieve(self, query: str, limit: int = 10):
        """Retrieve documents from Qdrant based on a query."""
        query_vector = self.get_embedding(query)  # <-- usa el nombre correcto

        response = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,  # <-- usa query_vector, no query
            limit=limit
        )
        concatenated_content = "\n\n\n --- \n\n\n".join([
            hit.payload.get("text", "") for hit in response
        ])
        return concatenated_content