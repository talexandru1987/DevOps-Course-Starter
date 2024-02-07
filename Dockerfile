
FROM ubuntu:latest as base

#Install python
RUN apt-get update && apt-get install -y python3.9 python3-pip

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



# Development stage
FROM dependencies as development_env

# Install the development dependencies
RUN poetry install 

# Expose the Flask development port
EXPOSE 5000


# Production environment
FROM dependencies as production


# Set entry point
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:8000", "todo_app.app:create_app()"]

#Expose the port
EXPOSE 8000


# Development environment
FROM development_env as development

# Change the working directory to app directory
WORKDIR /app

# Set the entrypoint for the development environment
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]

# Enable Flask debug mode
ENV FLASK_ENV=development


# Enable auto-relode when code changes
ENV FLASK_RUN_RELOAD=1

# Expose the flask development port
EXPOSE 5000


# # Test environment
FROM dependencies as test

RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip jq
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
  && CHROME_VERSIONS_JSON=$(wget --no-verbose -O - "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json") \
  && CHROME_DRIVER_VERSION=$(echo $CHROME_VERSIONS_JSON | jq -r ".milestones.\"${CHROME_MAJOR_VERSION}\".version") \
  && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_DRIVER_VERSION}/linux64/chromedriver-linux64.zip \
  && unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
  && mv /usr/bin/chromedriver-linux64/* /usr/bin \
  && rm -r /tmp/chromedriver_linux64.zip /usr/bin/chromedriver-linux64/ \
  && chmod 755 /usr/bin/chromedriver

ENTRYPOINT poetry run pytest