import os
import logging
from backend.core.schemas.config_schemas import ConfigModel
from backend.handlers.rag_handler import RAGHandler
from backend.utils import load_config_yaml
from backend.logging import configure_application

configure_application()

logger = logging.getLogger(__name__)

def main():
    # Load configuration (adjust the path to your config.yml if needed)
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend/config.yml'))
    config: ConfigModel = load_config_yaml(config_path)

    # Initialize the RAG handler
    rag_handler = RAGHandler(config)

    data_path = 'data/interim/'
    data = sorted(os.listdir(data_path))


    output_dir = 'data/artifacts'
    os.makedirs(output_dir, exist_ok=True)

    for file in data:
        if file.endswith('.pdf'):
            pdf_path = os.path.join(data_path, file)

            logger.info(f"Loading and indexing PDF: {pdf_path}")
            rag_handler.load(pdf_path, output_dir)
            logger.info("PDF loaded and indexed.")
        else:
            logger.info(f"Skip file {file}")


if __name__ == "__main__":
    main() 