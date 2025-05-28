from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Element
import logging

logger = logging.getLogger(__name__)

class PDFDataExtractor:

    @staticmethod
    def extract_elements(file_path: str, output_dir: str) -> list[Element]:
        """Extract images, tables, and chunk text from a PDF file.

        Args:
            file_path: Path to the PDF file
            output_dir: Directory to store extracted images
        Returns:
            List of unstructured document elements
        """
        logger.info(f"Extracting elements from PDF: {file_path}")
        elements = partition_pdf(
            filename=file_path,
            extract_images_in_pdf=True,
            strategy='hi_res',
            extract_image_block_types=["Image", "Table"],
            infer_table_structure=True,
            chunking_strategy="by_title",
            extract_image_block_to_payload=False,
            image_output_dir_path=output_dir,
        )
        logger.info(f"Extracted {len(elements)} elements from PDF.")
        return elements
    
    @staticmethod
    def categorize_elements(raw_pdf_elements: list[Element]) -> tuple[list[str], list[str]]:
        """Categorize extracted elements from a PDF into tables and texts.

        Args:
            raw_pdf_elements: List of unstructured.documents.elements
        Returns:
            Tuple of (texts, tables) where both are lists of strings
        """
        logger.info(f"Categorizing {len(raw_pdf_elements)} PDF elements.")
        tables = []
        texts = []
        for element in raw_pdf_elements:
            if "unstructured.documents.elements.Table" in str(type(element)):
                tables.append(str(element))
            elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
                texts.append(str(element))
        logger.info(f"Categorized into {len(texts)} texts and {len(tables)} tables.")
        return texts, tables
