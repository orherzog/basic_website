# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script and requirements.txt into the container
COPY google_search.py /app/
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Accept environment variables for API key and CSE ID
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}
ENV GOOGLE_CSE_ID=${GOOGLE_CSE_ID}

# Run the Python script when the container starts
CMD ["python", "google_search.py"]