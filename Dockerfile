FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && \
    apt-get install -y pkg-config python3-dev build-essential default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install -r requirements.txt
RUN pip install mysqlclient

COPY src src
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 CMD curl -f http://localhost:5000/health || exit 1
ENTRYPOINT ["python", "./src/app.py"]
