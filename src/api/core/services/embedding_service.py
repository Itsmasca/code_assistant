import csv
import io
import time
import uuid
import fitz  
import docx
import pandas as pd
from typing import Optional, Dict, List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class EmbeddingService:
    def __init__(self, client, embedding_model):
        self._client = client
        self._embedding_model = embedding_model
        self._text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.__collection_name = "code_assistant_knowledge_base"

    def _extract_text(self, file_bytes: bytes, file_type: str) -> str:
        if file_type == "application/pdf":
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            return "\n".join([page.get_text() for page in doc])
        elif file_type == "text/plain":
            return file_bytes.decode("utf-8")
        elif file_type == "text/csv":
            decoded = file_bytes.decode("utf-8")
            reader = csv.reader(io.StringIO(decoded))
            return "\n".join([", ".join(row) for row in reader])
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            doc = docx.Document(io.BytesIO(file_bytes))
            return "\n".join([p.text for p in doc.paragraphs])
        elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(io.BytesIO(file_bytes))
            return df.to_csv(index=False)
        elif file_type == "text/markdown":
            return file_bytes.decode("utf-8")
        else:
            return file_bytes.decode("utf-8", errors="ignore")

    async def embed_uploaded_document(
        self,
        file_bytes: bytes,
        file_type: str,
        filename: str,
        file_id: uuid.UUID,
        custom_metadata: Optional[Dict] = None,
    ) -> Dict:
        text = self._extract_text(file_bytes, file_type)
        documents = [Document(page_content=text, metadata={"filename": filename})]
        chunks = self._text_splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        embeddings = await self._embedding_model.aembed_documents(texts)

        timestamp = int(time.time())
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            metadata = {
                "upload_timestamp": timestamp,
                **chunk.metadata
            }

            if custom_metadata:
                metadata.update(custom_metadata)

            points.append({
                "id": str(uuid.uuid4()),
                "vector": embedding,
                "payload": {
                    "text": chunk.page_content,
                    "metadata": metadata
                }
            })

        self._client.upsert(collection_name=self.__collection_name, points=points)

        return {
            "status": "success",
            "chunks_processed": len(points),
            "collection": self.__collection_name,
            "document_id": str(file_id)
        }


    async def search_for_context(
        self,
        input: str,
        tok_k: int = 4
    ) -> List[Document]:
        query_embedding = await self._embedding_model.aembed_query(input)

        search_results = self._client.search(
            collection_name=self.__collection_name,
            query_vector=query_embedding,
            limit=tok_k,
            with_payload=True
        )

        if not search_results:
            return None

        docs =  [
            Document(
                page_content=item.payload["text"]
            ) for item in search_results
        ]

        return  "\n\n".join([doc.page_content for doc in docs])
