import logging
from backend.core.schemas.config_schemas import ConfigModel
from backend.core.ai.multimodal_rag import MultimodalRAG

logger = logging.getLogger(__name__)

class RAGHandler:
    """
    Handler for RAG (Retrieval-Augmented Generation) operations.
    Provides methods to load documents and answer queries using the RAG pipeline.
    """
    def __init__(self, config: ConfigModel):
        """
        Initialize the RAGHandler with the given configuration.

        Args:
            config (ConfigModel): The application configuration.
        """
        self.rag = MultimodalRAG(config)
        logger.info("RAGHandler initialized.")

    def load(self, pdf_path: str, output_dir: str) -> None:
        """
        Load and index a PDF document for RAG processing.

        Args:
            pdf_path (str): Path to the PDF file to ingest.
            output_dir (str): Directory to store extracted images and intermediate files.
        """
        logger.info(f"Loading and indexing PDF: {pdf_path}")
        self.rag.process_pdf(pdf_path, output_dir)
        logger.info("PDF loaded and indexed successfully.")

    def query(self, user_query: str) -> str:
        """
        Answer a user query using the indexed data and the RAG pipeline.

        Args:
            user_query (str): The user's question.

        Returns:
            str: The generated answer.
        """
        logger.info(f"Processing query: {user_query}")
        answer = self.rag.generate_answer(user_query)
        logger.info("Query processed and answer generated.")
        return answer 