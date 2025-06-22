import logging

import weaviate
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.schema import Document
from langchain_weaviate.vectorstores import WeaviateVectorStore

from backend.settings import get_settings


logger = logging.getLogger(__name__)


class MultiModalWeaviateRetriever:
    """Multi-modal retriever for Weaviate vector database."""

    def __init__(self, embeddings, collection_name: str):
        self._collection_name = collection_name
        self._settings = get_settings()
        self.embeddings = embeddings
        self.client = self._init_client()
        self.vector_store = self._init_vector_store()

    def _init_client(self) -> weaviate.WeaviateClient:
        """Initialize Weaviate client."""
        client = weaviate.connect_to_local()
        if not client.is_ready():
            raise ConnectionError(
                "Weaviate client is not ready. Check your Weaviate server."
            )
        return client

    def _init_vector_store(self) -> WeaviateVectorStore:
        """Initialize Weaviate vector store."""
        self.client.connect()
        return WeaviateVectorStore(
            client=self.client,
            index_name=self._collection_name,
            embedding=self.embeddings,
            text_key="text",
            attributes=["source"],
        )

    def delete_collection(self) -> None:
        """Delete all data from vector store collection"""
        self.client.collections.delete(self._collection_name)

    def add_documents(
        self, texts: list[str], metadatas: list[dict] | None = None
    ) -> None:
        """Add text documents to the vector store and memory store."""
        logger.info("Adding %d text documents to the vector store.", len(texts))
        try:
            self.vector_store.from_texts(
                texts=texts,
                embedding=self.embeddings,
                client=self.client,
                index_name=self._collection_name,
                text_key="text",
                metadatas=metadatas,
            )
        except Exception as error:
            logger.error("Error loading excel data: %s", error)
            raise error

        logger.debug("Documents successfully added.")

    def retrieve(self, query: str, top_k: int = 3) -> list[Document]:
        """Retrieve the most relevant documents for a given query.

        Args:
            query: The query string.
            top_k: Number of top results to return.

        Returns:
            List of relevant Document objects.
        """
        logger.info("Retrieving top %d documents for query: %s", top_k, query)
        results = self.vector_store.similarity_search(query, top_k)
        results = list(results)
        logger.debug("Retrieved %d documents.", len(results))
        return results

    def __del__(self):
        """Ensure the Weaviate client is closed when the retriever is deleted."""
        self.client.close()
