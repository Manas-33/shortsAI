
# Backend Dockerfile for Django
FROM python:3.11-slim

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY server/requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
# COPY ./server /app/
COPY server/ .


# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
