from backend.core.process_data.pdf_data_extractor import PDFDataExtractor
from backend.core.process_data.data_processor import DataProcessor
from backend.core.processors.table_processor import TableProcessor
from backend.core.processors.image_processor import ImageProcessor
from backend.core.ai.prompts.generation_prompt_template import GENERATION_PROMPT_TEMPLATE
from backend.core.schemas.config_schemas import ConfigModel
from backend.core.ai.ai_service import AIService
from backend.core.ai.multivector_chroma import MultiModalChromaRetriever
from langchain_community.embeddings import HuggingFaceEmbeddings

from typing import List, Dict
import os
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
        self.vector_retriever = MultiModalChromaRetriever(self.embeddings, 
                                                          collection_name=database_paramters.collection_name,
                                                          id_key=database_paramters.id_key
                                                          )

    def process_pdf(self, pdf_path: str, output_dir: str):
        """Extract and process text, tables, and images from a PDF, then index them in the vector database.

        Args:
            pdf_path: Path to the PDF file.
            output_dir: Directory to store extracted images.
        """
        logger.info(f"Processing PDF: {pdf_path}")

        elements = PDFDataExtractor.extract_elements(pdf_path, output_dir)
        texts, tables = PDFDataExtractor.categorize_elements(elements)
        logger.debug(f"Extracted {len(texts)} texts and {len(tables)} tables from PDF.")

        self.text_chunks = self.data_processor.tokenize_texts(texts)
        logger.debug(f"Tokenized text into {len(self.text_chunks)} chunks.")

        self.table_summaries = self.table_processor.summarize_tables(tables)
        logger.debug(f"Generated {len(self.table_summaries)} table summaries.")

        self.image_paths = [
            os.path.join(output_dir, f) for f in os.listdir(output_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        self.image_summaries = self.image_processor.summarize_images(self.image_paths)
        logger.debug(f"Generated {len(self.image_summaries)} image summaries.")

        self.vector_retriever.index_all(
            text_summaries=self.text_chunks, texts=self.text_chunks,
            table_summaries=self.table_summaries, tables=self.table_summaries,
            image_summaries=self.image_summaries, images=self.image_summaries
        )
        logger.info("PDF processing and indexing complete.")

    def retrieve_context(self, query: str, top_k: int = 3) -> Dict[str, List[str]]:
        """Retrieve relevant text, table, and image contexts for a given query from the vector database.

        Args:
            query: The user query string.
            top_k: Number of top results to retrieve.

        Returns:
            Dictionary with keys 'text', 'tables', and 'images' mapping to lists of relevant content.
        """
        logger.info(f"Retrieving context for query: {query}")
        docs = self.vector_retriever.retrieve(query, top_k=top_k)
        text_results, table_results, image_results = [], [], []
        for doc in docs:
            content = doc.page_content
            if content in self.text_chunks:
                text_results.append(content)
            elif content in self.table_summaries:
                table_results.append(content)
            elif content in self.image_summaries:
                image_results.append(content)
        logger.debug(f"Context retrieved: {len(text_results)} texts, {len(table_results)} tables, {len(image_results)} images.")
        return {
            'text': text_results,
            'tables': table_results,
            'images': image_results
        }

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
            text_context="\n".join(context['text']),
            table_context="\n".join(context['tables']),
            image_context="\n".join(context['images']),
            user_query=query
        )
        answer = self.ai_service.send_request(
            config=self.config,
            prompt=prompt,
            image_path=None,
        )
        logger.info("Answer generated.")
        return answer 