# Use the official Python image as a base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Set environment variables required by your application
ENV GRADIO_ANALYTICS_ENABLED=0

# Expose the port that Vercel or other services expect the app to run on
EXPOSE 8080

# Run the app
CMD ["python", "facefusion.py", "run"]
