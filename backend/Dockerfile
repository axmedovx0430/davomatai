FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for InsightFace and OpenCV
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    cmake \
    libopencv-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download InsightFace models
COPY download_models.py .
RUN python download_models.py

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p uploads/faces uploads/attendance

# Set environment variables to limit memory usage
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV VECLIB_MAXIMUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1

# Expose port
EXPOSE 8080

# Run application
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
