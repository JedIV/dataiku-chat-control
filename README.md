# Dataiku Chat Control

Control Dataiku DSS through Claude Code using an MCP server.

## Overview

This project provides an MCP (Model Context Protocol) server that enables Claude Code to perform actions on Dataiku DSS via chat, including:

- Building and deploying projects
- Managing datasets, recipes, and scenarios
- Creating and training ML models
- Running jobs and scenarios
- Importing SQL tables from connections

## Quick Start

### 1. Install Dependencies

```bash
cd mcp-server
pip install -r requirements.txt
```

Or with a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r mcp-server/requirements.txt
```

### 2. Configure Claude Code

Add the MCP server to your Claude Code configuration. Edit `~/.claude/mcp_settings.json`:

```json
{
  "mcpServers": {
    "dataiku": {
      "command": "python",
      "args": ["/path/to/dataiku-chat-control/mcp-server/server.py"],
      "env": {
        "DATAIKU_URL": "https://your-instance.dataiku.com",
        "DATAIKU_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Replace:
- `/path/to/dataiku-chat-control` with the actual path to this repo
- `https://your-instance.dataiku.com` with your Dataiku DSS URL
- `your-api-key-here` with your Dataiku API key

### 3. Get Your API Key

In Dataiku DSS:
1. Go to your profile (top right) → **API Keys**
2. Click **+ Create New API Key**
3. Give it a name and appropriate permissions
4. Copy the key (you won't see it again)

### 4. Restart Claude Code

After updating the MCP settings, restart Claude Code for the changes to take effect.

## Usage

Once configured, you can ask Claude to interact with Dataiku:

```
"List all projects in Dataiku"
"Create a new project called MY_PROJECT"
"Build the customers dataset in PROJECT_X"
"Show me the schema of the sales dataset"
```

## Available Helpers

The MCP server provides these helper functions:

### Jobs & Building
- `build_and_wait(client, project_key, dataset_name)` - Build a dataset
- `run_scenario_and_wait(client, project_key, scenario_id)` - Run a scenario
- `run_recipe_and_wait(client, project_key, recipe_name)` - Run a recipe
- `compute_and_apply_schema(client, project_key, recipe_name)` - Apply schema updates (required after modifying recipes)

### Data Inspection
- `dataset_info(client, project_key, dataset_name)` - Get dataset details
- `project_summary(client, project_key)` - Get project overview
- `connection_info(client, connection_name)` - Get connection details

### Search
- `find_datasets(client, pattern)` - Search for datasets
- `find_recipes(client, pattern)` - Search for recipes
- `find_by_connection(client, connection_name)` - Find datasets using a connection

### Data Export
- `to_records(client, project_key, dataset_name, limit=100)` - Get rows as dicts
- `head(client, project_key, dataset_name, n=5)` - Preview first rows
- `get_schema(client, project_key, dataset_name)` - Get column schema

## Important Notes

### Schema Updates
After creating or modifying a recipe, you **must** compute and apply schema before building:
```python
from helpers.jobs import compute_and_apply_schema
compute_and_apply_schema(client, "PROJECT", "recipe_name")
```

### Join Column Names
When joining datasets, output columns get prefixed with double underscores:
- `web.ip` becomes `web__ip`
- Left table columns keep original names

## Documentation

- [Dataiku Developer Guide](https://developer.dataiku.com/latest/index.html)
- [Python API Reference](https://developer.dataiku.com/latest/api-reference/python/client.html)
- [MCP Protocol](https://modelcontextprotocol.io/)
