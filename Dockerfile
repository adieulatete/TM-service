# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Run migrations and start the server
CMD python task_manager/manage.py makemigrations && python task_manager/manage.py migrate && python task_manager/manage.py runserver 0.0.0.0:8000
