# Use specific Python version
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose port
EXPOSE 5000

# Command to run your app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]