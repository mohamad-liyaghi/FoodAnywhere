FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apk update && apk add gcc musl-dev &&  apk add linux-headers

# Upgrade pip
RUN pip install --upgrade pip

# Install project dependencies
COPY requirements.txt /src/
RUN pip install -r /src/requirements.txt

# Copy the application code
COPY . /src/

WORKDIR /src

EXPOSE 8000
