from backend.core.ai.prompts.summary_tables_prompt import SUMMARY_TABLES_PROMPT
from backend.core.schemas.config_schemas import ConfigModel
from backend.core.ai.ai_service import AIService
import logging

logger = logging.getLogger(__name__)

class TableProcessor:
    """Processor for handling tables, including summarization."""
    def __init__(self, config: ConfigModel):
        self.config = config
        self.ai_service = AIService()

    def summarize_tables(self, tables: list[str]) -> list[str]:
        """Summarize a list of tables using the AI service.

        Args:
            tables: List of table strings to summarize.

        Returns:
            List of summarized table strings.
        """
        logger.info(f"Summarizing {len(tables)} tables.")
        results = [
            self.ai_service.send_request(
                config=self.config,
                system_prompt=SUMMARY_TABLES_PROMPT,
                user_prompt=table,
                image_path=None,
                model=self.config.types_of_models.llm_name
            ) for table in tables
        ]
        logger.info("Table summarization complete.")
        return results
