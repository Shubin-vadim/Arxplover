import os
from backend.core.schemas.config_schemas import ConfigModel
from backend.handlers.rag_handler import RAGHandler
from backend.utils import load_config_yaml
from backend.logging import configure_application

configure_application()

def main():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend/config.yml'))
    config: ConfigModel = load_config_yaml(config_path)

    rag_handler = RAGHandler(config)

    query_ru = 'Какой вклад вносит представленное исследование в автоматическое исправление уязвимостей кода, и какую роль в этом играют большие языковые модели (LLMs)?**'
    response = rag_handler.query(query_ru)
    print(response)


if __name__ == "__main__":
    main()