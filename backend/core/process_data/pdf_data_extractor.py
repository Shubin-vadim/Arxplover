from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import TableItem, PictureItem, TextItem

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFDataExtractor:
    
    @staticmethod
    def extract_elements(file_path: str, output_dir: str) -> dict:
        """
        Extract elements (tables, pictures, text) from a PDF file using Docling.

        Args:
            file_path: Path to the PDF file.
            output_dir: Directory to save extracted images and tables.

        Returns:
            Dict with lists of texts, tables, and image paths.
        """
        logger.info(f"Extracting elements from PDF using Docling: {file_path}")
        
        IMAGE_RESOLUTION_SCALE = 2.0
        pipeline_options = PdfPipelineOptions()
        pipeline_options.images_scale = IMAGE_RESOLUTION_SCALE
        pipeline_options.generate_page_images = True
        pipeline_options.generate_picture_images = True

        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        conv_res = doc_converter.convert(Path(file_path))
        doc_filename = conv_res.input.file.stem

        texts = []
        tables = []
        images = []

        table_counter = 0
        picture_counter = 0

        for element, _level in conv_res.document.iterate_items():
            if isinstance(element, TableItem):
                table_counter += 1
                table_df = element.export_to_dataframe()
                tables.append(table_df.to_markdown(index=False))

                # Save table image (optional)
                element_image_filename = Path(
                    f"{output_dir}/{doc_filename}-table-{table_counter}.png"
                )
                with element_image_filename.open("wb") as fp:
                    element.get_image(conv_res.document).save(fp, "PNG")
                images.append(str(element_image_filename))

            elif isinstance(element, PictureItem):
                picture_counter += 1
                element_image_filename = Path(
                    f"{output_dir}/{doc_filename}-picture-{picture_counter}.png"
                )
                with element_image_filename.open("wb") as fp:
                    element.get_image(conv_res.document).save(fp, "PNG")
                images.append(str(element_image_filename))

            else:
                # Handle other element types like text
                if isinstance(element, TextItem):
                    texts.append(element.text)

        logger.info(f"Extracted {len(texts)} text blocks, {len(tables)} tables, and {len(images)} images.")
        return {
            "texts": texts,
            "tables": tables,
            "images": images
        }

    @staticmethod
    def categorize_elements(elements_dict: dict) -> tuple[list[str], list[str], list[str]]:
        """
        Categorize extracted elements into texts, tables and images.

        Args:
            elements_dict: Dictionary returned by extract_elements method.

        Returns:
            Tuple of (texts, tables, images), all lists of strings.
        """
        logger.info("Categorizing extracted elements.")
        return (
            elements_dict["texts"],
            elements_dict["tables"],
            elements_dict["images"]
        )