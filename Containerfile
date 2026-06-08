FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY github_ai_genius ./github_ai_genius
RUN python -m pip install --upgrade pip && pip install -e .
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "github_ai_genius.api:app", "--host", "0.0.0.0", "--port", "8080"]
