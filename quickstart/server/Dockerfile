FROM python:3.12-slim
WORKDIR /app

# Download and install uv binary directly
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy only dependency files first (better caching)
COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock

# Install dependencies with uv
RUN uv sync --frozen

# Copy application code (changes more often)
COPY ./app.py /app/app.py

CMD ["python", "app.py"]