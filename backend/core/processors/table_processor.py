import logging

from backend.core.ai.ai_service import AIService
from backend.core.ai.prompts.summary_tables_prompt import SUMMARY_TABLES_PROMPT
from backend.core.schemes.config_schemes import ConfigModel


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
        logger.info("Summarizing %d tables.", len(tables))
        results = [
            self.ai_service.send_request(
                system_prompt=SUMMARY_TABLES_PROMPT,
                user_prompt=table,
                image_path=None,
                model=self.config.types_of_models.llm_name,
                temperature=self.config.llm_parameters.temperature
            )
            for table in tables
        ]
        logger.info("Table summarization complete.")
        return results
