# ArXplorer - Multimodal PDF Document Analysis System

ArXplorer is a comprehensive multimodal RAG (Retrieval-Augmented Generation) system for analyzing PDF documents with support for extracting and processing text, tables, and images using artificial intelligence.

## Key Features

### Enhanced PDF Processing
- **Text Extraction**: Intelligent chunking and processing of textual content
- **Table Processing**: Automatic table detection and analysis
- **Image Processing**: Complete extraction and analysis of images including:
  - Image classification (charts, diagrams, tables, formulas, photographs, screenshots)
  - Text extraction from images (OCR)
  - Chart and diagram data analysis
  - Scientific image interpretation
  - Detailed metadata extraction

### Multimodal AI Analysis
- **Image Classification**: Automatic categorization of images by type
- **Content Analysis**: Extraction of insights from charts, diagrams, and scientific figures
- **Text Recognition**: OCR for text within images
- **Scientific Context**: Specialized analysis for academic and research documents

### Vector Database Integration
- Indexes all content types (text, tables, images) for semantic search
- Retrieval-augmented generation for comprehensive answers
- Cross-modal query capabilities

## Project Structure

```
MultimodalRAG/
├── backend/                    # Main application logic
│   ├── core/                   # System core
│   │   ├── ai/                 # AI services and models
│   │   │   ├── multimodal_rag.py      # Main RAG orchestrator
│   │   │   ├── ai_service.py          # AI API interface
│   │   │   ├── multivector_chroma.py  # Vector database
│   │   │   └── prompts/               # Specialized prompts
│   │   ├── processors/         # Content processors
│   │   │   ├── image_processor.py     # Enhanced image analysis
│   │   │   └── table_processor.py     # Table processing
│   │   ├── process_data/       # Data extraction
│   │   │   ├── pdf_data_extractor.py  # PDF parsing with images
│   │   │   └── data_processor.py      # Text chunking
│   │   └── schemas/            # Configuration schemas
│   ├── handlers/               # High-level interfaces
│   │   ├── rag_handler.py      # Main RAG interface
│   │   └── rag_example.py      # Usage examples
│   ├── config.yml              # System configuration
│   ├── settings.py             # Application settings
│   ├── utils.py                # Utilities
│   └── logging.py              # Logging system
├── frontend/                   # Web interface
│   ├── frontend.py             # Chainlit web application
│   └── test_chainlit.py        # Interface tests
├── tests/                      # Tests
│   ├── test_unstructed.py      # PDF processing tests
│   └── test_unstructed_simple.py
├── scripts/                    # Scripts
│   └── code_quality_check.sh   # Code quality checks
├── setup.py                    # Package configuration
├── setup.cfg                   # Installation settings
└── .pylintrc                   # Linter configuration
```

## Installation

### Requirements
- Python 3.10+
- OpenAI API key
- Internet access for model downloads

### Step-by-step Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-repo/MultimodalRAG.git
cd MultimodalRAG
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -e .
```

4. **Set up environment variables:**
Create a `.env` file in the project root:
```env
LLM_API_KEY=your_openai_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
```

5. **Configure settings:**
Edit `backend/config.yml` if necessary:
```yaml
chunking:
  chunk_size: 700
  chunk_overlap: 140

types_of_models:
  llm_name: openai/gpt-4o-2024-05-13
  mm_llm_name: openai/gpt-4o-2024-05-13
  embedding_model_name: intfloat/multilingual-e5-large-instruct

vector_database_parameters:
  collection_name: mm_rag_vectorstore
  top_k: 5
```

## Usage

### Web Interface (Chainlit)

Start the web application:
```bash
cd frontend
chainlit run frontend.py
```

Open your browser and navigate to `http://localhost:8000`

### Programmatic Interface

#### Basic PDF Processing

```python
from backend.handlers.rag_handler import RAGHandler
from backend.utils import load_config_yaml

# Load configuration
config = load_config_yaml('backend/config.yml')
rag_handler = RAGHandler(config)

# Process PDF with image extraction
pdf_path = 'document.pdf'
output_dir = 'extracted_content'
rag_handler.load(pdf_path, output_dir)

# Get answer to a question
answer = rag_handler.query("What are the main conclusions presented in the document?")
print(answer)
```

#### Direct MultimodalRAG Usage

```python
from backend.core.ai.multimodal_rag import MultimodalRAG
from backend.core.schemas.config_schemas import ConfigModel

# Create configuration
config = ConfigModel(
    chunking={"chunk_size": 700, "chunk_overlap": 140},
    types_of_models={
        "llm_name": "openai/gpt-4o-2024-05-13",
        "mm_llm_name": "openai/gpt-4o-2024-05-13",
        "embedding_model_name": "intfloat/multilingual-e5-large-instruct"
    },
    vector_database_parameters={
        "collection_name": "mm_rag_vectorstore",
        "top_k": 5
    }
)

# Initialize RAG system
rag = MultimodalRAG(config)

# Process PDF
rag.process_pdf("document.pdf", "output_dir")

# Generate answer
answer = rag.generate_answer("Describe the charts in the document")
print(answer)
```

## Configuration

### Main Parameters

#### Chunking (Text Splitting)
```yaml
chunking:
  chunk_size: 700        # Text chunk size
  chunk_overlap: 140     # Overlap between chunks
```

#### AI Models
```yaml
types_of_models:
  llm_name: openai/gpt-4o-2024-05-13              # Text model
  mm_llm_name: openai/gpt-4o-2024-05-13           # Multimodal model
  embedding_model_name: intfloat/multilingual-e5-large-instruct  # Embedding model
```

#### Vector Database Parameters
```yaml
vector_database_parameters:
  collection_name: mm_rag_vectorstore  # Collection name
  id_key: doc_id                       # Document key
  top_k: 5                            # Number of search results
```

## Code Quality Checks
```bash
# Run all checks
./scripts/code_quality_check.sh

# Or individually
flake8
isort .
black .
mypy backend
pylint backend
```

## Image Processing Capabilities

### Supported Image Types
- **Charts/Graphs**: Bar charts, line graphs, pie charts, scatter plots
- **Diagrams**: Flowcharts, schematics, process diagrams
- **Tables**: Data tables, comparison matrices
- **Formulas**: Mathematical equations, chemical formulas
- **Photographs**: Microscopy, experimental setups
- **Screenshots**: Software interfaces, simulation results

### Analysis Features
- **Text Extraction**: OCR for all visible text, labels, and values
- **Data Analysis**: Trend identification, pattern recognition
- **Scientific Interpretation**: Context-aware analysis for research documents
- **Metadata Extraction**: File paths, dimensions, and technical details

## API Reference

### RAGHandler Methods

#### Core Processing
- `load(pdf_path, output_dir)`: Process PDF and extract all content
- `query(user_query)`: Query across all content types

### MultimodalRAG Methods

#### Document Processing
- `process_pdf(pdf_path, output_dir)`: Process PDF and index in vector database
- `retrieve_context(query, top_k)`: Retrieve relevant context for query
- `generate_answer(query)`: Generate answer using LLM

### ImageProcessor Methods

#### Image Processing
- `resize_images(image_paths, size)`: Resize images
- `summarize_images(image_paths, resize, size)`: Summarize images using AI

## Deployment

### Local Deployment
```bash
# Install dependencies
pip install -e .

# Start web interface
cd frontend
chainlit run frontend.py
```

### Docker Deployment
```bash
# Build image
docker build -t arxplorer .

# Run container
docker run -p 8000:8000 -e LLM_API_KEY=your_key arxplorer
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Use `black` for formatting
- Follow `flake8` for code style
- Add types with `mypy`

##License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Unstructured](https://github.com/Unstructured-IO/unstructured) for PDF processing
- Uses [LangChain](https://github.com/langchain-ai/langchain) for RAG capabilities
- Powered by OpenAI's multimodal models for image analysis
- Web interface built with [Chainlit](https://github.com/Chainlit/chainlit)

## Support

- **Author**: Vadim Shubin
- **Email**: vadyusha.shubin.2001@mail.ru
- **Issues**: [GitHub Issues](https://github.com/your-repo/MultimodalRAG/issues)
