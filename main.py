import os

import chainlit as cl

from backend.core.schemes.config_schemes import ConfigModel
from backend.handlers.rag_handler import RAGHandler
from backend.handlers.security_handler import SecurityHandler
from backend.handlers.image_handler import ImageHandler
from backend.logging import configure_application
from backend.utils import extract_json_from_string, load_config_yaml


configure_application()


@cl.set_starters
async def set_starters():
    """Starter for the chatbot."""
    return [
        cl.Starter(
            label="Определение LLM",
            message="Что такое LLM?",
        ),
        cl.Starter(
            label="Агентные системы",
            message="Какие основные компоненты и механизмы в LLM-агентах для построения одноагентных и многоагентных систем?",
        ),
        cl.Starter(
            label="Problems with long contexts",
            message="What are the problems with using long contexts in large language models?",
        ),
        cl.Starter(
            label="Methods for Alignment",
            message="What methods exist for aligning visual and textual representations?",
        ),
    ]

@cl.set_chat_profiles
async def chat_profile():
    """Chat profile for the chatbot."""
    return [
        cl.ChatProfile(
            name="GPT-4o-mini",
            markdown_description="Model for getting a quick answer.",
        ),
        cl.ChatProfile(
            name="GPT-4o",
            markdown_description="Model for a more accurate and generalized answer.",
        ),
    ]

@cl.on_message
async def main(msg: cl.Message) -> None:
    """Main function for handling incoming messages."""
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "backend/config.yml")
    )
    config: ConfigModel = load_config_yaml(config_path)

    if msg.elements:
        image_path = msg.elements[0].path
        image_handler = ImageHandler(config)
        image_description = image_handler.description_image(image_path)
        query = f'Image description: {image_description}\n\nUser question: {msg.content}'
    else:
        query = msg.content

    security_handler = SecurityHandler(config)
    response_security = security_handler.classification(query)

    response_security = extract_json_from_string(response_security)

    if response_security["harmful"]:
        response = response_security["response"]
    else:
        rag_handler = RAGHandler(config)

        response = rag_handler.query(query)

    await cl.Message(content=response).send()
