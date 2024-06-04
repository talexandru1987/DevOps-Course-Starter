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

The CONNECTION_STRING in the `.env` needs to
be completed with the secure link for azure cosmos DB.

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
dropdawn option containing the available boards from the mongo DB.
After choosing a board the
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

## Create Azure WebApp

Portal:

Create a Resource -> Web App
Select your project resource group.
In the “Publish” field, select “Docker Container”
Configure a service plan.
On the next screen, select Docker Hub in the “Image Source” field, and enter the details of your image.

CLI:

First create an App Service Plan:

```
az appservice plan create --resource-group <resource_group_name> -n <appservice_plan_name> --sku B1 --is-linux
```

Then create the Web App:

```
az webapp create --resource-group <resource_group_name> --plan <appservice_plan_name> --name <webapp_name> --deployment-container-image-name docker.io/<dockerhub_username>/<container-image-name>:latest

```

## Setup environment variables from your .env file

Portal:
Settings -> Configuration in the Portal
Add all the environment variables as “New application setting”

CLI
Enter them individually via

```
az webapp config appsettings set -g <resource_group_name> -n <webapp_name> --settings FLASK_APP=todo_app/app.

```

The app works on port 8000, so create a “New application setting” called WEBSITES_PORT with the value 8000

## Deployed app

```
https://anothertodo.azurewebsites.net/

```

## Continuous Deployment

When there is a push to Main and the pipeline test passes, the new code is automatically deployed to Azure.

## Connecting to CosmosDB

In your terminal, ensure that the Poetry package manager is available by using this command in your terminal:

```
poetry shell
```

Open the interpreter in your terminal by typing:

```
python
```

In your interpreter, type the following commands and replace 'connection string' with your actual database connection string found in Azure:

```
import pymongo
client = pymongo.MongoClient("connection string")
client.list_database_names()
```

## Setting up the app Authentication using GitHub

## Setting Up GitHub OAuth

After setting up the application in GitHub, you need to add the details to this section of the .env file:

```
Copy code
OAUTH_ID=
OAUTH_KEY=
OAUTH_URL=
ENV=
```

The ENV variable is a flag to indicate whether you are running locally or not. Leave it blank in this case.

If you need to run the application locally with GitHub OAuth, add the details to this section of the .env file:

```
Copy code
OAUTH_ID_L=
OAUTH_KEY_L=
OAUTH_URL_L=
ENV=Local
```

Set the ENV variable to Local so the appropriate variables are used for OAuth.

If you need to disable authentication for testing purposes, update the LOGIN_DISABLED variable in the .env file to True or False.
