# FROM python:3.9-alpine as base

# FROM python:3.8-slim-buster as base

FROM ubuntu:latest as base

#Install python
RUN apt-get update && apt-get install -y python3 python3-pip

# Set environment variable
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install poetry
RUN pip install poetry

# Set up the working directory
WORKDIR /app

# Copy the content of the repo inside the image
COPY . /app



# Dependecies stage
FROM base as dependencies

# Install dependecies withtout the dev dependencies
RUN poetry install --no-dev

RUN pip install Flask gunicorn


# Development stage
FROM dependencies as development_env

# Install the development dependencies
RUN poetry install 

# Expose the Flask development port
EXPOSE 5000


# Production environment
FROM dependencies as production

#copy the dependencies
COPY --from=dependencies /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

#copy the application code from the dependencies stage
COPY --from=dependencies /app /app 

# Set entry point
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "todo_app.app:create_app()"]

#Expose the port
EXPOSE 8000


# Development environment
FROM development_env as development

# Change the working directory to app directory
WORKDIR /app

# Set the entrypoint for the development environment
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# Enable Flask debug mode
ENV FLASK_ENV=development


# Enable auto-relode when code changes
ENV FLASK_RUN_RELOAD=1

# Expose the flask development port
EXPOSE 5000


# # Test environment
FROM dependencies as test


ENTRYPOINT poetry run pytest todo_app/tests