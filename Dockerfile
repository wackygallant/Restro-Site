# 1. Use a lightweight Python version
FROM python:3.13-slim

# 2. Set environment variables
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout/stderr (better for Docker logs)
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies
# We install 'libpq-dev' and 'gcc' so we can compile Postgres drivers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
# We copy requirements.txt first to take advantage of Docker's cache layers
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your project code
COPY . /app/

# 7. Final Command
# This is a fallback. Your docker-compose.yml 'command' will override this.
# Replace 'restro_site' with your actual project folder name
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
