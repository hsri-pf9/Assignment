FROM python:3.9

WORKDIR /app

COPY server.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "server.py"]
