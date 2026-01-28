# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This project enables Claude Code to control Dataiku DSS through the Python API. The goal is to perform administrative and user actions via chat, including:
- Adjusting admin settings
- Building and deploying projects
- Managing datasets, recipes, and scenarios
- User and group management
- Any operation available through the Dataiku API

## Architecture

Claude Code writes and executes Python scripts that call the Dataiku API (`dataiku-api-client` package) to perform actions on the configured Dataiku instance.

```
User Request → Claude Code → Python Script → dataikuapi → Dataiku DSS Instance
```

### Key Files
- `client.py` - Provides `get_client()` function that returns a configured `DSSClient`
- `.env` - Contains credentials (gitignored, never commit)
- `.env.example` - Template showing required environment variables

## Setup

```bash
# Set Python version and create virtual environment
pyenv local 3.10.14
python -m venv venv

# Activate and install dependencies
source venv/bin/activate  # or: ./venv/bin/pip install -r requirements.txt
pip install -r requirements.txt
```

Required environment variables in `.env`:
- `DATAIKU_URL` - Base URL of Dataiku instance (e.g., `https://instance.dataiku.com`)
- `DATAIKU_API_KEY` - API key with appropriate permissions

## Common Commands

```bash
# Test connection
./venv/bin/python client.py

# Run any script
./venv/bin/python <script.py>
```

## Using the Dataiku API

### Basic Pattern
```python
from client import get_client

client = get_client()

# List projects
projects = client.list_project_keys()

# Get a specific project
project = client.get_project("PROJECT_KEY")

# Access datasets, recipes, scenarios from the project
datasets = project.list_datasets()
```

### Key API Objects

| Object | Access Pattern | Common Operations |
|--------|---------------|-------------------|
| Project | `client.get_project(key)` | list_datasets, list_recipes, list_scenarios |
| Dataset | `project.get_dataset(name)` | get_settings, read data, write data |
| Recipe | `project.get_recipe(name)` | get_settings, run |
| Scenario | `project.get_scenario(id)` | run, get_status |
| Admin | `client.get_general_settings()` | system configuration |
| Users | `client.list_users()` | user management |

### Admin Operations
```python
# Get general settings
settings = client.get_general_settings()

# List all users
users = client.list_users()

# Create a user
client.create_user(login, password, display_name)

# List code environments
envs = client.list_code_envs()
```

## API Documentation

- **Developer Guide**: https://developer.dataiku.com/latest/index.html
- **Python API Reference**: https://developer.dataiku.com/latest/api-reference/python/client.html
- **GitHub Source**: https://github.com/dataiku/dataiku-api-client-python

## Workflow for Claude Code

When asked to perform a Dataiku action:

1. Import the client: `from client import get_client`
2. Create client instance: `client = get_client()`
3. Navigate to the appropriate API object (project, dataset, etc.)
4. Perform the operation
5. Return results or confirmation

For exploratory tasks, print intermediate results to understand the current state before making changes.

## Skills (Reusable Scripts)

### Create Dataset (`create_dataset.py`)

Create a managed dataset with CSV data.

```bash
# From a CSV file
./venv/bin/python create_dataset.py PROJECT_KEY dataset_name data.csv

# From JSON
./venv/bin/python create_dataset.py PROJECT_KEY dataset_name '{"columns": ["id", "name"], "rows": [[1, "Alice"], [2, "Bob"]]}'
```

**Python usage:**
```python
from create_dataset import create_dataset_from_records

records = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]
create_dataset_from_records("PROJECT_KEY", "my_dataset", records)
```

### Import SQL Table (`import_sql_table.py`)

Import a table from a SQL connection (Snowflake, etc.) with automatic schema detection.

```bash
# Import with auto-generated name
./venv/bin/python import_sql_table.py PROJECT_KEY sf-azure CRM CUSTOMERS

# Import with custom dataset name
./venv/bin/python import_sql_table.py PROJECT_KEY sf-azure CRM CUSTOMERS my_customers
```

**Python usage:**
```python
from import_sql_table import list_schemas, list_tables, import_table, get_dataset_info

# Explore available schemas and tables
schemas = list_schemas("sf-azure", "PROJECT_KEY")
tables = list_tables("sf-azure", "CRM", "PROJECT_KEY")

# Import a table
import_table("PROJECT_KEY", "sf-azure", "CRM", "CUSTOMERS", "my_customers")

# Get dataset info
info = get_dataset_info("PROJECT_KEY", "my_customers")
print(info['columns'])  # [(name, type), ...]
print(info['sample'])   # [row_dict, ...]
```
