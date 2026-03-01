# Use a base Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install necessary system dependencies (GLPK, CBC, etc.) and Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends glpk-utils coinor-cbc unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    unzip -oq assets/demo-data/CLEWs.Demo.zip -d /app && \
    pip install --no-cache-dir --upgrade -r requirements.txt 

# Expose the port for Flask app
EXPOSE 5002

ENV PORT=5002 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Start via waitress
CMD ["sh", "-c", "cd API && python -m waitress --host=0.0.0.0 --port=${PORT} app:app"]
