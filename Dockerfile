FROM python:3.14-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY . .

# Create data directory if not exists
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]