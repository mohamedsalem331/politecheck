FROM python:3.12-slim 

# Set environment variables
# PYTHONUNBUFFERED=1: Log output immediately (important in Docker)
# PYTHONDONTWRITEBYTECODE=1: Prevents writing .pyc files (not useful in containers)
# PIP_NO_CACHE_DIR=1: Don’t cache installed packages (saves space)
# PIP_DISABLE_PIP_VERSION_CHECK=1: Disables pip version warnings
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 

# Install system dependencies
# Updates package lists
# Installs curl (used later or for debugging)
# --no-install-recommends keeps it minimal
# Deletes cached package lists to reduce image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.7.1

# Set work directory
WORKDIR /app
ENV PYTHONPATH=/app/src

# Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies using Poetry export to requirements
# Exports dependencies from Poetry into a plain requirements.txt
# Installs them using pip (this is faster and avoids installing Poetry-managed virtualenvs)
# Deletes the file afterward to keep the image clean

RUN poetry export -f requirements.txt --without-hashes --only=main -o requirements.txt \
    && pip install -r requirements.txt \
    && rm requirements.txt

# Copy application code
COPY src/ ./src/
COPY development.ini ./
COPY gunicorn.conf.py ./

# Create non-root user
RUN groupadd -r politecheck && useradd -r -g politecheck politecheck

# Set ownership
RUN chown -R politecheck:politecheck /app

# Switch to non-root user
USER politecheck

# Expose port
EXPOSE 8000


# Default command
CMD ["gunicorn", "--config", "gunicorn.conf.py", "politecheck.wsgi:app"]
