# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise
> (i.e. you cannot use your local machine) then
> you'll want to launch a VM using the
> [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter).
> Note this VM comes pre-setup with Python &
> Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an
isolated environment and manage package
dependencies. To prepare your system, ensure you
have an official distribution of Python version
3.8+ and install Poetry using one of the following
commands (as instructed by the
[poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate
package dependencies. To create the virtual
environment and install required packages, run the
following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from
the `.env.template` to store local configuration
options. This is a one-time operation on first
setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set
environment variables when running `flask run`.
This enables things like development mode (which
also enables features like hot reloading when you
make a file change). There's also a
[SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY)
variable which is used to encrypt the flask
session cookie.

The TRELLO_TOKEN, TRELLO_KEY in the `.env` need to
be completed with the secure credentials from your
trello account for the application to work.

## Running the App

Once the all dependencies have been installed,
start the Flask app in development mode within the
Poetry environment by running:

```bash
$ poetry run flask run
```

You should see output similar to the following:

```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

Now visit
[`http://localhost:5000/`](http://localhost:5000/)
in your web browser to view the app.

## Using the app

Whe the app starts the user will be presented with
dropdawn option containing the available boards on
their Trello account. After choosing a board the
app will render all the cards on the board.

### Testing

The application's tests, along with their
respective requirements, reside within the `test`
directory located at the project root.
Specifically:

- **Tests:** You can find the tests in the
  `test_view_model.py` file.
- **Fixtures:** Configuration for fixtures is
  housed in `conftest.py`.

For executing the tests, ensure that `pytest` is
installed. It's imperative to ensure consistent
environments between `pytest` and `poetry`. Hence,
kindly invoke the tests using:

```bash
poetry run pytest

```

### Provision a VM from an Asible Control Node

1. Create the files todoapp.service, .env.j2,
   alex-ansible-playbook.yml and
   alex-inventory.txt in the Controler Node

2. Update the files with the relevan details for
   your VM:
   - .env.j2 : update the path of the poetry
     install file if needed
   - alex-inventory.txt : add the ip addresses for
     the VM's in scope
3. Run the Ansible playboak in the Controle node

```
ansible-playbook alex-ansible-playbook.yml -i alex-invetory

```

4.  when running the playbook you will be asked
    for the access tokens

5.  Navigate to http://host.ip.address:5000/ to
    see the output

### Creating a production or development Docker image

The Dockerfile contains the multi stage build
sequence to create a production or development
image using Docker

## Production Docker image build

1. Build the image using:

```
docker build --target production --tag todo-app:prod .

```

2. Run the image using:

```
docker run --env-file .env -p 8000:8000 todo-app:prod .

```

## Development Docker image build using docker commands

1. Build the image using:

```
docker build --target development --tag todo-app:dev .

```

2. To use a bind mount when running the container
   and make the “todo_app” directory on the host
   machine available as a mounted directory. Build
   by using the following syntax:

```
docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev

```

## Development Docker image build using docker compose

1. Build the image using:

```
docker compose up

```

## CI pipline trigger

The settings for the CI pipline are included in:

```
.github/workflows/my-ci-pipeline.yml

```

The CI pipline will trigger if:

1. There is a push request
2. There is a pull request with the main branch
3. It's Sunday at 00:00

The CI pipline will not trigger on push or pull request if the changes involve only the README.md file

When running the CI pipline will:

1. Run all the unit and end to end tests
2. Send the code to Snyk to check for vulnerabilities

## Put Container Image on Docker Hub registry

Build the docker image where "yourID" is your docker id. If you need to use the development image change the string "prod" to "dev":

```
docker build --target production --tag yourID/todo-app:prod .

```

Make shure you are connected to docker by using:

```
docker login

```

Push the image by using:

```
docker push yourID/todo-app:prod

```
