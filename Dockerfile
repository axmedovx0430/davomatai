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

# Copy only backend directory
COPY backend/ .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create uploads directory
RUN mkdir -p uploads/faces uploads/attendance

# Expose port
EXPOSE 8080

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
