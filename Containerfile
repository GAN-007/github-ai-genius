FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY github_ai_genius ./github_ai_genius

RUN python -m pip install --upgrade pip && \
    pip install -e .

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "github_ai_genius.api_v2:app", "--host", "0.0.0.0", "--port", "8080"]
