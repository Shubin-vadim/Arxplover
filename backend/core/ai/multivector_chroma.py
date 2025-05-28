import uuid
from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.documents import Document
from typing import List, Any
import logging

logger = logging.getLogger(__name__)

class MultiModalChromaRetriever:
    def __init__(self, embeddings, 
                 persist_directory: str = "./chroma_db", 
                 collection_name: str = "mm_rag_vectorstore", 
                 id_key: str = "doc_id"
                 ):
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        self.store = InMemoryStore()
        self.id_key = id_key
        self.retriever = MultiVectorRetriever(
            vectorstore=self.vectorstore,
            docstore=self.store,
            id_key=self.id_key,
        )

    def add_documents(self, doc_summaries: List[str], doc_contents: List[Any]):
        """Add documents and their summaries to the vector store and document store.

        Args:
            doc_summaries: List of summary strings for the documents.
            doc_contents: List of original document contents.
        """
        logger.info(f"Adding {len(doc_summaries)} documents to the vector store.")
        doc_ids = [str(uuid.uuid4()) for _ in doc_contents]
        summary_docs = [
            Document(page_content=s, metadata={self.id_key: doc_ids[i]})
            for i, s in enumerate(doc_summaries)
        ]
        self.retriever.vectorstore.add_documents(summary_docs)
        self.retriever.docstore.mset(list(zip(doc_ids, doc_contents)))
        logger.debug("Documents added to vector and doc store.")

    def index_all(self, text_summaries=None, texts=None, table_summaries=None, tables=None, image_summaries=None, images=None):
        """Index all provided summaries and contents into the vector store.

        Args:
            text_summaries: List of text summaries.
            texts: List of original texts.
            table_summaries: List of table summaries.
            tables: List of original tables.
            image_summaries: List of image summaries.
            images: List of original images.
        """
        logger.info("Indexing all provided data into the vector store.")
        if text_summaries and texts:
            self.add_documents(text_summaries, texts)
        if table_summaries and tables:
            self.add_documents(table_summaries, tables)
        if image_summaries and images:
            self.add_documents(image_summaries, images)
        logger.info("Indexing complete.")

    def retrieve(self, query: str, top_k: int = 3):
        """Retrieve the most relevant documents for a given query.

        Args:
            query: The query string.
            top_k: Number of top results to return.

        Returns:
            List of relevant Document objects.
        """
        logger.info(f"Retrieving top {top_k} documents for query: {query}")
        results = self.retriever.get_relevant_documents(query)[:top_k]
        logger.debug(f"Retrieved {len(results)} documents.")
        return results 