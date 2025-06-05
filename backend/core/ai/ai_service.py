from openai import OpenAI
from backend.settings import get_settings
import base64
from backend.core.schemas.config_schemas import ConfigModel
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )

    def send_request(
        self,
        config: ConfigModel,
        system_prompt: str,
        user_prompt: str | None = None,
        image_path: str | None = None,
        model: str = "openai/gpt-4o-2024-05-13",
    ) -> str:
        """
        Sends a request (text or text + image) to OpenAI.

        Args:
            config (ConfigModel): The configuration model.
            prompt (str): The text prompt to send.
            image_path (str, optional): Path to the image file (jpg/png). If None, sends only text.
            model (str): OpenAI model name.

        Returns:
            str: The model's response.
        """
        logger.info(f"Sending request to OpenAI model '{model}'.")
        if image_path:
            # Read and encode the image in base64
            with open(image_path, "rb") as img_file:
                img_b64 = base64.b64encode(img_file.read()).decode("utf-8")

            # Build the multimodal message
            messages = [
                {"role": "system", 
                 "content": [
                     {
                         "type": "text", 
                         "text": system_prompt
                         }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_b64}"
                            }
                        }
                    ]
                },
            ]
        else:
            if user_prompt is None:
                messages = [
                    {
                        "role": "system",
                        "content": [{"type": "text", "text": system_prompt}]
                    }
                ]
            else:
                messages = [
                    {
                        "role": "system",
                        "content": [{"type": "text", "text": system_prompt}]
                    },
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": user_prompt}]
                    }
                ]

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=config.llm_parameters.temperature,
        )
        logger.info("Received response from OpenAI.")
        return response.choices[0].message.content

