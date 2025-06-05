import chainlit as cl

import os
from ..backend.core.schemas.config_schemas import ConfigModel
from ..backend.handlers.rag_handler import RAGHandler
from ..backend.utils import load_config_yaml
from ..backend.logging import configure_application

configure_application()

@cl.on_message
async def main(msg: cl.Message) -> None:

    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend/config.yml'))
    config: ConfigModel = load_config_yaml(config_path)

    rag_handler = RAGHandler(config)

    response = rag_handler.query(msg.content)

    await cl.Message(content=f'Response: {response}').send()
