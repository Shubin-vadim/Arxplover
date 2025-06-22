FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -e .

EXPOSE 8080

CMD ["chainlit", "run", "main.py", "-w"]