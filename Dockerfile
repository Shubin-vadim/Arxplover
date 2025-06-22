# Base image
FROM python:3.12-slim

# Environment variables for the application
ENV PYTHONUNBUFFERED=1 \
    CHAINLIT_HOST=0.0.0.0 \
    CHAINLIT_PORT=8000

# Create working directory
WORKDIR /app

# Copy project files and install Python dependencies
# Copying and installing in a single layer for simplicity (no caching)
COPY . .
RUN pip install --no-cache-dir .

# Expose port for the application
EXPOSE 8000

# Command to run the application
CMD ["chainlit", "run", "frontend/frontend.py", "--port", "8000"]
