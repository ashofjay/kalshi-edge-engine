FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY data ./data
ENV PYTHONPATH=/app/src
CMD ["sh", "-c", "uvicorn kalshi_edge_engine.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
