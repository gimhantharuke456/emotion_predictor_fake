# Use the official Python image as the base image
FROM python:3.10

# Install required system dependencies for OpenCV
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
# Install required Python packages
RUN pip install -r requirements.txt

# Set the working directory inside the container
WORKDIR /app

# Copy the app files into the container
COPY main.py .

# Expose the port on which the FastAPI app will run
EXPOSE 8003

# Start the FastAPI server using uvicorn when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8003"]
