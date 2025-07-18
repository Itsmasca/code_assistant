from qdrant_client import QdrantClient
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