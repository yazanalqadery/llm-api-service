# FROM python:3.12-slim
# WORKDIR /app
# # COPY main.py .
# COPY . .
# RUN pip install fastapi uvicorn pydantic-settings
# # CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
# # RUN uvicorn main:app --host 0.0.0.0 --port 8000

FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
RUN useradd --create-home appuser
USER appuser
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]