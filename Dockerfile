FROM python:3.11-slim

WORKDIR /app

# system deps (build tools for any wheels that need them)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install core deps. Heavy NLP libs (torch/transformers/spacy) are commented
# in requirements.txt by default to keep the image lean — uncomment them there
# to bake FinBERT into the image.
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
# Default command runs the API. Override to run the dashboard.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
