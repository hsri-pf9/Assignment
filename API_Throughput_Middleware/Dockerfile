# Dockerfile
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install dependencies
RUN pip install flask
RUN pip install requests

# Expose ports for both servers
EXPOSE 3001
EXPOSE 3002

# Run the main script
CMD ["python", "main.py"]
