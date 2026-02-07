# Dataiku MCP Server

An MCP server that enables Claude to control Dataiku DSS through Python code execution.

## Architecture

Instead of exposing dozens of individual tools, this server exposes a single `execute_python` tool that runs Python code with a pre-configured Dataiku client. This follows Anthropic's ["code execution with MCP"](https://www.anthropic.com/engineering/code-execution-with-mcp) pattern.

```
Claude → execute_python(code) → Python interpreter with:
                                - Pre-configured DSSClient
                                - Helper modules
                                - Persistent state
```

## Installation

```bash
cd mcp-server
pip install -r requirements.txt
```

Configure instances in the parent directory (repo root) by creating
`.dataiku-instances.json` (copy from the example):

```bash
cp ../.dataiku-instances.example.json ../.dataiku-instances.json
```

Edit `../.dataiku-instances.json` with your instance details.

## Usage with Claude Code

Add to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "dataiku": {
      "command": "python",
      "args": ["/path/to/mcp-server/server.py"]
    }
  }
}
```

## Tools

### `execute_python`

Execute Python code with the Dataiku client pre-configured.

**Available in namespace:**
- `client` - Authenticated DSSClient instance
- `helpers.jobs` - Async operation handling
- `helpers.inspection` - Data exploration
- `helpers.search` - Cross-project discovery
- `helpers.export` - Data extraction

**Example:**
```python
# List all projects
print(client.list_project_keys())

# Get project summary
from helpers.inspection import project_summary
print(project_summary(client, "MY_PROJECT"))
```

### `list_helpers`

List all available helper functions with their signatures.

## Helper Modules

### `helpers.jobs`

Handle async operations with polling:

```python
from helpers.jobs import build_and_wait, run_scenario_and_wait

# Build a dataset
result = build_and_wait(client, "PROJECT", "dataset_name")
print(result)  # {'success': True, 'status': 'DONE', 'duration': 12.5, ...}

# Run a scenario
result = run_scenario_and_wait(client, "PROJECT", "scenario_id")
```

### `helpers.inspection`

Explore data quickly:

```python
from helpers.inspection import dataset_info, project_summary

# Get dataset details
info = dataset_info(client, "PROJECT", "my_dataset")
print(info['schema'])
print(info['sample'])

# Get project overview
summary = project_summary(client, "PROJECT")
print(f"{summary['dataset_count']} datasets, {summary['recipe_count']} recipes")
```

### `helpers.search`

Find things across projects:

```python
from helpers.search import find_datasets, find_by_connection

# Find datasets by name pattern
results = find_datasets(client, "customer.*")

# Find all datasets using a connection
results = find_by_connection(client, "my_snowflake_conn")
```

### `helpers.export`

Extract data:

```python
from helpers.export import to_records, head, get_schema

# Get data as list of dicts
rows = to_records(client, "PROJECT", "dataset", limit=100)

# Print first few rows
head(client, "PROJECT", "dataset", n=5)

# Get schema
schema = get_schema(client, "PROJECT", "dataset")
```

## State Persistence

Variables persist across `execute_python` calls within the same session:

```python
# First call
projects = client.list_project_keys()
my_project = client.get_project(projects[0])

# Second call - my_project still exists
datasets = my_project.list_datasets()
```

## Direct API Access

The full Dataiku API is available through `client`:

```python
# Admin operations
users = client.list_users()
connections = client.list_connections()

# Project operations
project = client.get_project("MY_PROJECT")
datasets = project.list_datasets()
recipes = project.list_recipes()

# Dataset operations
dataset = project.get_dataset("my_dataset")
settings = dataset.get_settings()
```

See [Dataiku Python API docs](https://developer.dataiku.com/latest/api-reference/python/client.html) for full reference.
