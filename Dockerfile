FROM python:3.9-alpine as base

FROM base as dependencies
# Set environment variable
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install poetry
RUN pip install poetry

# Copy the content of the repo inside the image
COPY . /app

# Install Flask and gunicorn
RUN pip install Flask gunicorn

#install app dependencies
WORKDIR /app
RUN poetry install --no-dev



#production environment
FROM base as production

#copy the dependencies
COPY --from=dependencies /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

#copy the app
COPY --from=dependencies /app /app

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "todo_app.app:create_app()"]

EXPOSE 8000
