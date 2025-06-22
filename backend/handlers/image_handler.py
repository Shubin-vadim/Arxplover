import logging

from backend.core.ai.ai_service import AIService
from backend.core.schemes.config_schemes import ConfigModel
from backend.core.ai.prompts.summary_images_prompt import SUMMARY_IMAGES_PROMPT, USER_IMAGES_PROMPT

logger = logging.getLogger(__name__)

class ImageHandler:
    """
    Handler for image operations.
    Provides methods to load images and perform image-related tasks.
    """
    def __init__(self, config: ConfigModel):
        self.ai_service = AIService()
        self.config = config
        logger.info("ImageHandler initialized.")

    def description_image(self, image_path: str) -> str:
        """
        Generate a description of the image using OpenAI.
        :param image_path: Path to the image file.
        :return: Description of the image.
        """
        logger.info("Generating description for image: %s", image_path)
        response = self.ai_service.send_request(
            system_prompt=SUMMARY_IMAGES_PROMPT, 
            user_prompt=USER_IMAGES_PROMPT,
            image_path=image_path,
            model=self.config.types_of_models.mm_llm_name,
            temperature=self.config.mm_llm_parameters.temperature,
            )


        return response

    
