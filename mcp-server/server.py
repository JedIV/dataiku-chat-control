#!/usr/bin/env python3
"""Dataiku MCP Server - Code Execution Paradigm.

This MCP server exposes a single tool that executes Python code with a
pre-configured Dataiku client and helper modules. This follows the
"code execution with MCP" pattern for maximum flexibility and minimal
token overhead.

Usage:
    python server.py
"""

import sys
import os
from io import StringIO
from pathlib import Path
from textwrap import dedent

# Add paths for imports
server_dir = Path(__file__).parent
parent_dir = server_dir.parent
sys.path.insert(0, str(parent_dir))  # For client.py
sys.path.insert(0, str(server_dir))  # For helpers package

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv(parent_dir / ".env")

# Check for required credentials
_dataiku_url = os.environ.get("DATAIKU_URL")
_dataiku_api_key = os.environ.get("DATAIKU_API_KEY")
_credentials_missing = not _dataiku_url or not _dataiku_api_key

# Import after path setup
from client import get_client
import helpers
from helpers import jobs, inspection, search, export

# Build instructions based on credential status
if _credentials_missing:
    _instructions = dedent("""
    ⚠️  DATAIKU CREDENTIALS NOT CONFIGURED

    The Dataiku MCP server requires DATAIKU_URL and DATAIKU_API_KEY to be set.

    To configure, edit your Claude Code MCP settings (~/.claude/mcp_settings.json):

    {
      "mcpServers": {
        "dataiku": {
          "command": "python",
          "args": ["/path/to/mcp-server/server.py"],
          "env": {
            "DATAIKU_URL": "https://your-instance.dataiku.com",
            "DATAIKU_API_KEY": "your-api-key-here"
          }
        }
      }
    }

    To get an API key in Dataiku: Profile → API Keys → Create New API Key

    After updating, restart Claude Code for changes to take effect.
    """).strip()
else:
    _instructions = dedent("""
    Dataiku DSS control server. Use the execute_python tool to run Python code
    with a pre-configured Dataiku client.

    Available in the execution namespace:
    - client: Authenticated DSSClient instance
    - helpers.jobs: Build/scenario waiting (build_and_wait, run_scenario_and_wait, compute_and_apply_schema)
    - helpers.inspection: Data exploration (dataset_info, project_summary)
    - helpers.search: Cross-project search (find_datasets, find_by_connection)
    - helpers.export: Data extraction (to_records, sample, head)

    Example:
        # List all projects
        print(client.list_project_keys())

        # Get project summary
        from helpers.inspection import project_summary
        print(project_summary(client, "MY_PROJECT"))

        # Build a dataset and wait
        from helpers.jobs import build_and_wait
        result = build_and_wait(client, "MY_PROJECT", "my_dataset")
        print(result)

    IMPORTANT: After creating or modifying a recipe, you MUST compute and apply schema
    before building, or the build will fail with missing column errors:
        from helpers.jobs import compute_and_apply_schema
        compute_and_apply_schema(client, "PROJECT", "recipe_name")

    IMPORTANT: When joining datasets, output columns get prefixed with the input dataset
    name and double underscore. For example, joining 'crm' and 'web' datasets:
    - 'web.ip' becomes 'web__ip' (double underscore)
    - 'crm.customer_id' stays 'customer_id' (left table keeps original names)
    """).strip()

# Initialize MCP server
mcp = FastMCP("dataiku", instructions=_instructions)

# Initialize the Dataiku client
_client = None

def get_dataiku_client():
    """Get or create the Dataiku client singleton."""
    global _client
    if _client is None:
        _client = get_client()
    return _client

# Persistent execution namespace
execution_globals = {
    "__builtins__": __builtins__,
    "helpers": helpers,
    "jobs": jobs,
    "inspection": inspection,
    "search": search,
    "export": export,
}


@mcp.tool()
def execute_python(code: str) -> str:
    """Execute Python code with pre-configured Dataiku client.

    The execution environment includes:
    - client: Authenticated DSSClient connected to your Dataiku instance
    - helpers.jobs: build_and_wait, run_scenario_and_wait, run_recipe_and_wait
    - helpers.inspection: dataset_info, project_summary, connection_info
    - helpers.search: find_datasets, find_recipes, find_by_connection
    - helpers.export: to_records, sample, head, get_schema

    Variables persist across calls within the same session.

    Args:
        code: Python code to execute

    Returns:
        stdout output from the code, or error message if execution fails
    """
    # Check for credentials
    if _credentials_missing:
        return dedent("""
        ERROR: Dataiku credentials not configured.

        Please add DATAIKU_URL and DATAIKU_API_KEY to your MCP server config.

        Edit ~/.claude/mcp_settings.json and add to the "dataiku" server:
          "env": {
            "DATAIKU_URL": "https://your-instance.dataiku.com",
            "DATAIKU_API_KEY": "your-api-key"
          }

        Then restart Claude Code.
        """).strip()

    # Ensure client is in namespace
    execution_globals["client"] = get_dataiku_client()

    # Capture stdout
    stdout_capture = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_capture

    try:
        # Execute the code
        exec(code, execution_globals)
        output = stdout_capture.getvalue()
        return output if output else "(executed successfully, no output)"
    except Exception as e:
        import traceback
        error_output = stdout_capture.getvalue()
        tb = traceback.format_exc()
        return f"{error_output}\nError: {type(e).__name__}: {e}\n\n{tb}"
    finally:
        sys.stdout = old_stdout


@mcp.tool()
def list_helpers() -> str:
    """List all available helper functions and their signatures.

    Returns:
        Formatted list of all helper modules and functions
    """
    output = []

    output.append("=== helpers.jobs ===")
    output.append("  build_and_wait(client, project_key, dataset_name, build_mode='RECURSIVE_BUILD', timeout=600)")
    output.append("  run_scenario_and_wait(client, project_key, scenario_id, timeout=600)")
    output.append("  run_recipe_and_wait(client, project_key, recipe_name, timeout=600)")
    output.append("  wait_for_job(job, timeout=600, poll_interval=2)")
    output.append("  get_job_log(client, project_key, job_id)")
    output.append("  compute_and_apply_schema(client, project_key, recipe_name)  # REQUIRED after creating/modifying recipes")
    output.append("")

    output.append("=== helpers.inspection ===")
    output.append("  dataset_info(client, project_key, dataset_name, sample_size=5)")
    output.append("  project_summary(client, project_key)")
    output.append("  list_projects_summary(client)")
    output.append("  connection_info(client, connection_name)")
    output.append("  list_connections_summary(client)")
    output.append("  user_info(client, login=None)")
    output.append("")

    output.append("=== helpers.search ===")
    output.append("  find_datasets(client, pattern, project_key=None)")
    output.append("  find_recipes(client, pattern, project_key=None)")
    output.append("  find_scenarios(client, pattern, project_key=None)")
    output.append("  find_by_connection(client, connection_name)")
    output.append("  find_by_type(client, dataset_type, project_key=None)")
    output.append("  find_users(client, pattern)")
    output.append("")

    output.append("=== helpers.export ===")
    output.append("  to_records(client, project_key, dataset_name, limit=100)")
    output.append("  sample(client, project_key, dataset_name, n=10)")
    output.append("  get_schema(client, project_key, dataset_name)")
    output.append("  get_column_names(client, project_key, dataset_name)")
    output.append("  count_rows(client, project_key, dataset_name)")
    output.append("  head(client, project_key, dataset_name, n=5)")
    output.append("  describe(client, project_key, dataset_name)")
    output.append("  to_csv_string(client, project_key, dataset_name, limit=100)")

    return "\n".join(output)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
