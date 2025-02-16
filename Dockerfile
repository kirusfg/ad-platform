# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    nodejs \
    npm \
    && apt-get clean

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set work directory
WORKDIR /app

RUN ls

# Copy project files
COPY pyproject.toml uv.lock README.md /app/
COPY apps/ /app/apps/
COPY config/ /app/config/

RUN ls -la

# Install Python dependencies using uv
RUN uv venv
RUN uv pip install -e .

COPY manage.py /app/

ENV OPENAI_API_KEY=later

RUN uv run manage.py migrate

ENV NO_NOTIFICATIONS=True
RUN uv run manage.py populate_db
ENV NO_NOTIFICATIONS=False

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@email.com
ENV DJANGO_SUPERUSER_PHONE_NUMBER=+1234567890
RUN uv run manage.py createsuperuser --noinput

# Install Node.js dependencies and build static files
COPY . /app/

RUN npm install
RUN npm run build

# Collect static files
RUN uv run manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

ENV DEBUG=False

# Run the Django application with Gunicorn
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]