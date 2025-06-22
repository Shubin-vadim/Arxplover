import logging

from backend.core.ai.ai_service import AIService
from backend.core.ai.prompts.security_prompt_template import SECURITY_PROMPT_TEMPLATE
from backend.core.schemes.config_schemes import ConfigModel


logger = logging.getLogger(__name__)


class SecurityHandler:
    """
    Handler for security-related operations.
    Provides methods to generate security-related prompts and check for security-related keywords.
    """

    def __init__(self, config: ConfigModel):
        self.ai_service = AIService()
        self.config = config
        logger.info("SecurityHandler initialized.")

    def classification(self, user_query: str) -> str:
        """
        Generate a security-related prompt based on the input text.

        Args:
            text (str): Input text for generating the prompt.

        Returns:
            str: The generated security-related prompt.
        """
        logger.info("Generating security prompt for: %s.", user_query)
        classification_prompt = SECURITY_PROMPT_TEMPLATE.format(
            user_question=user_query
        )
        response = self.ai_service.send_request(
            system_prompt=classification_prompt,
            model=self.config.types_of_models.llm_name,
            temperature=self.config.llm_parameters.temperature,
        )
        logging.info("Security prompt generated.")
        return response
