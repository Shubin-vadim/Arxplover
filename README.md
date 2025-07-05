# ArXplorer - Multimodal PDF Document Analysis System

ArXplorer is a comprehensive multimodal system for analyzing PDF documents with support for extracting and processing text, tables, and images using artificial intelligence.

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
chainlit run main.py -w
```

Open your browser and navigate to `http://localhost:8000`


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
```

## Deployment

### Local Deployment
```bash
# Install dependencies
pip install -e .

# Start web interface
cd frontend
chainlit run main.py -w
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

## License

This project is licensed under the Apache License 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Docling](https://github.com/docling-project/docling) for PDF processing
- Uses [LangChain](https://github.com/langchain-ai/langchain) for development
- Powered by OpenAI's multimodal models for image analysis
- Web interface built with [Chainlit](https://github.com/Chainlit/chainlit)

## Support

- **Author**: Vadim Shubin
- **Email**: vadyusha.shubin.2001@mail.ru
- **Issues**: [GitHub Issues](https://github.com/your-repo/MultimodalRAG/issues)
