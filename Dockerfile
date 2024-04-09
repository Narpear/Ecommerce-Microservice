FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

COPY src src
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 CMD curl -f http://localhost:5000/health || exit 1
ENTRYPOINT ["python", "./src/app.py"]
