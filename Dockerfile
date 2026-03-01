# Use a base Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Create non-root user
RUN useradd -m muiogo

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends glpk-utils coinor-cbc unzip && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Seed demo data
RUN unzip -oq assets/demo-data/CLEWs.Demo.zip -d /app

# Ensure correct ownership
RUN chown -R muiogo:muiogo /app

# Switch to non-root user
USER muiogo

EXPOSE 5002

ENV PORT=5002 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Start via waitress
CMD ["sh", "-c", "cd API && python -m waitress --host=0.0.0.0 --port=${PORT} app:app"]
