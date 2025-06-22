import logging
import os

from PIL import Image

from backend.core.ai.ai_service import AIService
from backend.core.ai.prompts.summary_images_prompt import (
    SUMMARY_IMAGES_PROMPT,
    USER_IMAGES_PROMPT,
)
from backend.core.schemes.config_schemes import ConfigModel


logger = logging.getLogger(__name__)


class ImageProcessor:
    """Processor for handling images, including resizing and summarization."""

    def __init__(self, config: ConfigModel):
        self.config = config
        self.ai_service = AIService()

    def resize_images(self, image_paths: list[str], size=(512, 512)) -> list[str]:
        """Resize all images to a single resolution. Returns paths to new images.

        Args:
            image_paths: List of image file paths to resize.
            size: Target size as a tuple (width, height).

        Returns:
            List of file paths to resized images.
        """
        logger.info("Resizing %d images to size %s.", len(image_paths), size)

        resized_paths = []
        for path in image_paths:
            img = Image.open(path)
            img = img.convert("RGB")
            img = img.resize(size)
            base, ext = os.path.splitext(path)
            new_path = f"{base}_resized{ext}"
            img.save(new_path)
            resized_paths.append(new_path)
        logger.info("Image resizing complete.")
        return resized_paths

    def summarize_images(
        self, image_paths: list[str], resize: bool = True, size=(512, 512)
    ) -> list[str]:
        """Summarize a list of images using the AI service.

        Args:
            image_paths: List of image file paths to summarize.
            resize: Whether to resize images before summarization.
            size: Target size for resizing.

        Returns:
            List of image summaries as strings.
        """
        if resize:
            logger.info("Resizing images before summarization.")
            image_paths = self.resize_images(image_paths, size=size)
        logger.info("Summarizing %d images.", len(image_paths))

        results = [
            self.ai_service.send_request(
                system_prompt=SUMMARY_IMAGES_PROMPT,
                user_prompt=USER_IMAGES_PROMPT,
                image_path=img_path,
                model=self.config.types_of_models.mm_llm_name,
                temperature=self.config.mm_llm_parameters.temperature
            )
            for img_path in image_paths
        ]
        logger.info("Image summarization complete.")
        return results
