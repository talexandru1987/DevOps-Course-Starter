FROM python:3.9-alpine as base

# Set environment variable
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install poetry
RUN pip install poetry Flask gunicorn

# Set up the working directory
WORKDIR /app

# Copy the content of the repo inside the image
COPY . /app



# Dependecies stage
FROM base as dependencies

# Install dependecies withtout the dev dependencies
RUN poetry install --no-dev


# Development stage
FROM dependencies as development_env

# Install the development dependencies
RUN poetry install 

# Expose the Flask development port
EXPOSE 5000


# Production environment
FROM base as production

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