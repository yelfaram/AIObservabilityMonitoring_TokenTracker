# python environment
FROM python:3.13-slim

# set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY rest of app
COPY . .

# Expose FastAPI port (documentation)
EXPOSE 8000

# command to run app
CMD ["uvicorn", "app.LLM_API_Logic:app", "--host", "0.0.0.0", "--port", "8000"]



