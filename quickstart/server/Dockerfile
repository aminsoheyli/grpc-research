FROM python:3.12-slim
WORKDIR /app

# Download and install uv binary directly
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy only dependency files first (better caching)
COPY . /app/


# Install dependencies with uv
RUN uv sync --frozen

CMD ["/bin/bash", "-c", "source .venv/bin/activate && python app.py"]