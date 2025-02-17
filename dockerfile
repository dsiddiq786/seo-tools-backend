# Use official Python image
FROM python:3.12.8

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install system dependencies required for Python and Postgres
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    gcc \
    g++ \
    cmake \
    make \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    libbz2-dev \
    zlib1g-dev \
    libjpeg-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    libopenjp2-7 \
    libpng-dev \
    libx11-6 \
    python3-dev \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel before installing dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the image background model (for rembg tool)
RUN wget -P /app "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"

# Expose the FastAPI app port
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]