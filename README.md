# Project Management CLI Tool

A simple Python-based command-line tool for managing users, projects, and tasks.

## Features

- Create and list users
- Add projects to a specific user
- Assign tasks to projects
- Mark tasks complete
- Persist data to `data.json`

## Installation

This tool uses `click` for command-line handling and `pytest` for tests.

Install dependencies with `pip`:

```bash
python3 -m pip install click pytest
```

Or use `pipenv` if you prefer:

```bash
pipenv install --dev
pipenv run pytest
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

To run with a custom file path:

```bash
python3 pm.py --data-file ./custom-data.json user list
```

## Tests

```bash
pytest
```

## Data storage

The tool stores data in `data.json` by default, or in the file specified by `--data-file`.
# python-project-management-cli-tool
