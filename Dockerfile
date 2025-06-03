# Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . .

# Expose Django port
EXPOSE 8000

# Default run command
CMD ["python", "_360groundproject/manage.py", "runserver", "0.0.0.0:8000"]
