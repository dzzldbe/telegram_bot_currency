FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Create non-root user early
RUN useradd -m botuser

WORKDIR /app

# Give botuser ownership of the workdir
RUN chown botuser:botuser /app

# Switch to non-root before installing
USER botuser

# Copy dependency files first (layer caching)
COPY --chown=botuser:botuser pyproject.toml uv.lock ./

# Install dependencies from lockfile
RUN uv sync --frozen --no-install-project

# Copy the rest of the app
COPY --chown=botuser:botuser . .

# Install the project itself
RUN uv sync --frozen

CMD ["uv", "run", "python", "bot.py"]
