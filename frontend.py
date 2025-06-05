import chainlit as cl

import os
from backend.core.schemas.config_schemas import ConfigModel
from backend.handlers.rag_handler import RAGHandler
from backend.utils import load_config_yaml
from backend.logging import configure_application

configure_application()

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Определение LLM",
            message="Что такое LLM?",
            # icon="/home/user/Desktop/folders/myself/MultimodalRAG/icons/llm.svg",
            ),

        cl.Starter(
            label="Агентные системы",
            message="Какие основные компоненты и механизмы в LLM-агентах для построения одноагентных и многоагентных систем?",
            # icon="/public/learn.svg",
            ),
        cl.Starter(
            label="Проблемы длинных контекстов",
            message="Какие проблемы возникают при использовании длинных контекстов в больших языковых моделях?",
            # icon="/public/terminal.svg",
            ),
        cl.Starter(
            label="Methods for Alignment",
            message="What methods exist for aligning visual and textual representations?",
            # icon="/public/write.svg",
            )
        ]

@cl.on_message
async def main(msg: cl.Message) -> None:

    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend/config.yml'))
    config: ConfigModel = load_config_yaml(config_path)

    rag_handler = RAGHandler(config)

    response = rag_handler.query(msg.content)

    await cl.Message(content=f'Response: {response}').send()
