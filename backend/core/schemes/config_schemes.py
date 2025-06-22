from pydantic import BaseModel


class ChunkingSettingsModel(BaseModel):
    """Configuration for text chunking parameters."""

    chunk_size: int
    chunk_overlap: int


class TypesOfModelsModel(BaseModel):
    """Configuration for model names used in the application."""

    llm_name: str
    mm_llm_name: str
    embedding_model_name: str


class LLMParametersModel(BaseModel):
    """Configuration for LLM (Large Language Model) parameters."""

    temperature: float


class MMLLMParametersModel(BaseModel):
    """Configuration for MM-LLM (Multi-Modal Large Language Model) parameters."""

    temperature: float


class VectorDataBaseModel(BaseModel):
    """Configuration for vector database parameters."""

    collection_name: str
    top_k: int


class ConfigModel(BaseModel):
    """Main configuration model containing all application settings."""

    chunking: ChunkingSettingsModel
    types_of_models: TypesOfModelsModel
    llm_parameters: LLMParametersModel
    mm_llm_parameters: MMLLMParametersModel
    vector_database_parameters: VectorDataBaseModel
