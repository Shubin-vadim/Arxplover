from backend.core.process_data.pdf_data_extractor import PDFDataExtractor
from backend.core.process_data.data_processor import DataProcessor
from backend.core.processors.table_processor import TableProcessor
from backend.core.processors.image_processor import ImageProcessor
from backend.core.ai.prompts.generation_prompt_template import GENERATION_PROMPT_TEMPLATE
from backend.core.schemas.config_schemas import ConfigModel
from backend.core.ai.ai_service import AIService
from backend.core.ai.multimodal_weatiate import MultiModalWeaviateRetriever
from langchain_community.embeddings import HuggingFaceEmbeddings

import logging

logger = logging.getLogger(__name__)

class MultimodalRAG:
    def __init__(self, config: ConfigModel):
        self.config = config
        self.data_processor = DataProcessor(config)
        self.table_processor = TableProcessor(config)
        self.image_processor = ImageProcessor(config)
        self.ai_service = AIService()
     
        self.text_chunks: list[str] = []
        self.table_summaries: list[str] = []
        self.image_summaries: list[str] = []
        self.image_paths: list[str] = []
     
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.types_of_models.embedding_model_name
        )
        database_paramters = config.vector_database_parameters
        self.vector_retriever = MultiModalWeaviateRetriever(self.embeddings, 
                                                          collection_name=database_paramters.collection_name,
                                                            )

    def process_pdf(self, pdf_path: str, output_dir: str):
        """Extract and process text, tables, and images from a PDF, then index them in the vector database.

        Args:
            pdf_path: Path to the PDF file.
            output_dir: Directory to store extracted images.
        """
        logger.info(f"Processing PDF: {pdf_path}")

        elements = PDFDataExtractor.extract_elements(pdf_path, output_dir)
        texts, tables, images = PDFDataExtractor.categorize_elements(elements)
        logger.debug(f"Extracted {len(texts)} texts and {len(tables)} tables from PDF.")

        text_chunks = self.data_processor.tokenize_texts(texts)
        logger.debug(f"Tokenized text into {len(text_chunks)} chunks.")

        table_summaries = self.table_processor.summarize_tables(tables)
        logger.debug(f"Generated {len(table_summaries)} table summaries.")

        table_chunks = self.data_processor.tokenize_texts(tables)
        logger.debug(f"Tokenized table into {len(table_chunks)} chunks.")
        
        image_summaries = self.image_processor.summarize_images(images)
        logger.debug(f"Generated {len(image_summaries)} image summaries.")

        images_chunks = self.data_processor.tokenize_texts(self.image_summaries)
        logger.debug(f"Tokenized image into {len(images_chunks)} chunks.")

        metadata_texts = [{'source':pdf_path}] * len(text_chunks)
        self.vector_retriever.add_documents(texts=text_chunks, metadatas=metadata_texts)
        logger.info("Text chunks added to vector store.")

        metadata_tables = [{'source':pdf_path}] * len(table_chunks)
        self.vector_retriever.add_documents(texts=table_chunks, metadatas=metadata_tables)
        logger.info("Table chunks added to vector store.")

        metadata_images = [{'source':pdf_path}] * len(images_chunks)
        self.vector_retriever.add_documents(texts=images_chunks, metadatas=metadata_images)
        logger.info("Image chunks added to vector store.")

        logger.info("PDF processing and indexing complete.")

    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """Retrieve relevant text, table, and image contexts for a given query from the vector database.

        Args:
            query: The user query string.
            top_k: Number of top results to retrieve.

        Returns:
            Dictionary with keys 'text', 'tables', and 'images' mapping to lists of relevant content.
        """
        logger.info(f"Retrieving context for query: {query}")
        docs = self.vector_retriever.retrieve(query, top_k=top_k)
        context = '\n'.join(doc.page_content for doc in docs)
        metadatas = [doc.metadata for doc in docs]

        return context

    def generate_answer(self, query: str) -> str:
        """Generate an answer to the user query using retrieved context and the LLM.

        Args:
            query: The user query string.

        Returns:
            The generated answer as a string.
        """
        logger.info(f"Generating answer for query: {query}")
        context = self.retrieve_context(query, self.config.vector_database_parameters.top_k)
        prompt = GENERATION_PROMPT_TEMPLATE.format(
            context=context,
            user_query=query
        )
        answer = self.ai_service.send_request(
            config=self.config,
            system_prompt=prompt,
            image_path=None,
        )
        logger.info("Answer generated.")
        return answer 