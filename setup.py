from setuptools import setup


version = "0.0.1"

setup(
    name="arxplover",
    version=version,
    description="arxplover app for analyze documents",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    author="Vadim Shubin",
    author_email="vadyusha.shubin.2001@mail.ru",
    include_package_data=True,
    install_requires=[
        "colorlog~=6.9.0",
        "chainlit~=2.5.5",
        "Sphinx~=8.2.3",
        "pdfminer~=20191125",
        "pillow~=11.2.1",
        "pydantic~=2.10.6",
        "pydantic-settings~=2.7.1",
        "python-dotenv~=1.0.1",
        "pytz~=2025.1",
        "furo~=2024.8.6",
        "langchain~=0.3.25",
        "langchain-chroma~=0.2.4",
        "langchain-openai~=0.3.17"
        "unstructured~=0.17.2"
    ],
    extras_require={
        "code-quality": [
            "asyncpg-stubs~=0.30.0",
            "black~=25.1.0",
            "flake8~=7.1.1",
            "isort~=6.0.0",
            "mypy~=1.15.0",
            "pylint~=3.3.4",
            "pylint_pydantic~=0.3.5",
            "types-pytz~=2025.1.0.20250204",
            "types-setuptools~=75.8.0.20250110",
        ],
        "testing": [
            "httpx~=0.28.1",
            "pytest~=8.3.4",
            "pytest_asyncio~=0.25.3",
        ],
    },
    packages=[],
    python_requires=">=3.10",
    keywords="multimodal rag arvix",
)
