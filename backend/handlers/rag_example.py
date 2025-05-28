import os
from backend.core.schemas.config_schemas import ConfigModel
from backend.handlers.rag_handler import RAGHandler
from backend.utils import load_config_yaml

# Example usage of RAGHandler

def main():
    # Load configuration (adjust the path to your config.yml if needed)
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config.yml'))
    config: ConfigModel = load_config_yaml(config_path)

    # Initialize the RAG handler
    rag_handler = RAGHandler(config)

    # Example PDF and output directory (replace with your actual files)
    pdf_path = 'example.pdf'  # Path to your PDF file
    output_dir = 'output_dir'  # Directory for extracted images and intermediate files
    os.makedirs(output_dir, exist_ok=True)

    # Load and index the PDF
    print(f"Loading and indexing PDF: {pdf_path}")
    rag_handler.load(pdf_path, output_dir)
    print("PDF loaded and indexed.")

    # Access and print extracted image paths
    image_paths = rag_handler.get_extracted_images()
    print(f"Extracted images ({len(image_paths)}):")
    for img_path in image_paths:
        print(f" - {img_path}")

    # Example user query
    user_query = "What is the main topic of the document?"
    print(f"Querying: {user_query}")
    answer = rag_handler.query(user_query)
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main() 