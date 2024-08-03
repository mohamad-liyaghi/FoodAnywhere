FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apk update && apk add gcc musl-dev &&  apk add linux-headers

# Install gdal-bin libgdal-dev python3-gdal
RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/community gdal-tools

# Upgrade pip
RUN pip install --upgrade pip

# Install project dependencies
COPY requirements.txt /src/
RUN pip install -r /src/requirements.txt

# Copy the application code
COPY . /src/

WORKDIR /src

EXPOSE 8000
