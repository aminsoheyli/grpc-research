FROM python:3.12
WORKDIR /app

# Install uv
RUN pip install uv

# Copy only dependency files first (better caching)
COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock

# Install dependencies with uv
RUN uv sync --frozen

# Copy application code (changes more often)
COPY ./app.py /app/app.py

CMD ["python", "app.py"]