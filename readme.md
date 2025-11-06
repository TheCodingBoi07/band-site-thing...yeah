# Rock Bands App

This is a Flask application with a SQLite database for demonstrating relational database principles.

## Running

- Set up a Python virtual environment

  ```pwsh
  python -m venv venv
  venv\scripts\activate
  ```

- Install project dependencies

  ```pwsh
  pip install -r requirements.txt
  ```

- Create your `.env` file

  ```pwsh
  cp .env-sample .env
  ```

- Run the app

  ```pwsh
  flask run --debug
  ```

## Developing Your Own Version

To develop your own version of this project, you can `clone` or `fork` this repo.

- `git clone <repo url>` makes a copy of the repo, but still considers the upstream (parent) repo to be this repo. This is fine for development and testing, but the remote repo still belongs to me.
- Forking the repo makes a copy of the repo on _your_ GitHub account, meaning that you have full control of it from that point forward. This is the better approach when you want to make your own version of an existing project, as opposed to contributing to the original one.
