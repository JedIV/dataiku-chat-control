# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Purpose

This project enables Claude Code to control Dataiku DSS through an MCP server. The MCP server provides a `client` object and helper functions for interacting with Dataiku.

## Using Dataiku

Use the `mcp__dataiku__execute_python` tool to run Python code. The execution environment includes:

- `client` - Authenticated DSSClient for the current instance
- `helpers.jobs` - Build and run operations
- `helpers.inspection` - Dataset and project info
- `helpers.search` - Find datasets, recipes, etc.
- `helpers.export` - Export data as records

### Examples

```python
# List projects
print(client.list_project_keys())

# Get project summary
from helpers.inspection import project_summary
print(project_summary(client, "PROJECT_KEY"))

# Build a dataset
from helpers.jobs import build_and_wait
build_and_wait(client, "PROJECT_KEY", "dataset_name")
```

### Multi-Instance Support

Use `mcp__dataiku__use_instance` to switch between configured instances.
Use `mcp__dataiku__list_instances` to see available instances.

## Important: Schema Updates

After creating or modifying a recipe, you **must** compute and apply schema before building:

```python
from helpers.jobs import compute_and_apply_schema
compute_and_apply_schema(client, "PROJECT", "recipe_name")
```

## Skills Reference

Before calling `mcp__dataiku__execute_python`, check the `skills/` folder for relevant API patterns. Each skill contains a `SKILL.md` with usage guidance and a `references/` folder with detailed code examples.

Available skills:

| Skill | When to consult |
|---|---|
| `recipe-patterns` | Creating or configuring recipes (prepare, join, group, sync, python) |
| `dataset-management` | Creating datasets, uploading files, managing schemas |
| `flow-management` | Building datasets, running pipelines, managing dependencies |
| `ml-training` | Training models, extracting metrics, deploying to flow |
| `data-catalog` | Working with metadata, tags, meanings, data collections |
| `troubleshooting` | Debugging failed jobs or diagnosing errors |

**Workflow:** Read the relevant `SKILL.md` first, then consult specific files under `references/` as needed before writing code. This ensures correct API usage and avoids common pitfalls.

## API Documentation

- [Developer Guide](https://developer.dataiku.com/latest/index.html)
- [Python API Reference](https://developer.dataiku.com/latest/api-reference/python/client.html)
