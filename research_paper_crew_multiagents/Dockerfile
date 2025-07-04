# ------------------------
# Stage 1: Builder
# ------------------------
FROM python:3.12-slim AS builder

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    python3-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app/research_paper_analyst

# Copy dependency file and install Python packages to /wheels
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ------------------------
# Stage 2: Runtime (Lightweight)
# ------------------------
FROM python:3.12-slim AS runtime

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app/research_paper_analyst

# Minimal system dependencies needed to run the app
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy built wheels and install them
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy source code (only once, cleanly)
COPY . .

# Set appropriate permissions
RUN chmod -R 777 /app/research_paper_analyst

# Expose the FastAPI port
EXPOSE 8000 8501

# Run the app
#CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run ui/future_predictor.py --server.port 8501 --server.address 0.0.0.0"]
