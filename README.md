# Project Management CLI Tool

A Python CLI application for managing users, projects, and tasks with persistent JSON storage.

## Features

- Create, list, and manage users
- Add projects and associate them with users
- Create tasks for projects with contributor assignments
- Mark tasks complete
- Persist all data in JSON with safe load/save behavior
- Support custom data file path (`--data-file`)

## Installation

A Python 3 environment is required.

### Using a virtual environment

```bash
cd python-project-management-cli-tool
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install click pytest
```

### Using pipenv

```bash
cd python-project-management-cli-tool
pipenv install --dev
pipenv shell
```

## Usage

Run the CLI from the repository root:

```bash
python3 pm.py user create --name "Alice" --email alice@example.com
python3 pm.py user list
python3 pm.py project add --user-id 1 --name "Website Redesign"
python3 pm.py project list --user-id 1
python3 pm.py task add --project-id 1 --title "Design mockups" --description "Build UI mockups" --contributors 1
python3 pm.py task list --project-id 1
python3 pm.py task complete --task-id 1
python3 pm.py task assign --task-id 1 --user-id 2
```

Use a custom file for persistence:

```bash
python3 pm.py --data-file ./custom-data.json user list
```

## Tests

Run the unit tests with:

```bash
pytest
```

If using the virtual environment:

```bash
.venv/bin/python -m pytest -q
```

## Data storage

By default, data is stored in `data.json` in the project root. You can override this with `--data-file`.

