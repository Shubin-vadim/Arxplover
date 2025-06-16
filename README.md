### Setting Up the Project Locally

1. Clone the repository:

```
git clone git@github.com/Shubin-vadim/MultimodalRAG
OR**

git clone https://github.com/Shubin-vadim/MultimodalRAG.git
```

2. Install Dependencies using Poetry:

```
cd MultimodalRAG && python3 -m venv .venv && source .venv/bin/activate
pip3 install -U pip setuptools
pip3 install -e .
pip3 install .[code-quality,testing]
```

## Usage
```
chainlit run frontend.py -w
```
