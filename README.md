# Dataiku Chat Control

Control Dataiku DSS through Claude Code using an MCP server.

## Quick Start

### 1. Install Dependencies

```bash
cd mcp-server
pip install -r requirements.txt
```

### 2. Configure Instances

Copy the example config and add your instances:

```bash
cp .dataiku-instances.example.json .dataiku-instances.json
```

Edit `.dataiku-instances.json`:

```json
{
  "default": "MyInstance",
  "instances": {
    "MyInstance": {
      "url": "https://your-instance.dataiku.com",
      "api_key": "dkuaps-your-api-key",
      "description": "My Dataiku instance"
    }
  }
}
```

### 3. Configure Claude Code

Add the MCP server to `~/.claude/mcp_settings.json`:

```json
{
  "mcpServers": {
    "dataiku": {
      "command": "python",
      "args": ["/path/to/dataiku-chat-control/mcp-server/server.py"]
    }
  }
}
```

### 4. Get Your API Key

In Dataiku DSS:
1. Go to your profile (top right) > **API Keys**
2. Click **+ Create New API Key**
3. Copy the key

### 5. Restart Claude Code

## Usage

Once configured, ask Claude to interact with Dataiku:

```
"List all projects in Dataiku"
"Build the customers dataset in PROJECT_X"
"Show me the schema of the sales dataset"
```

Switch instances with:
```
"Switch to the Analytics instance"
```

## Documentation

- [Dataiku Developer Guide](https://developer.dataiku.com/latest/index.html)
- [Python API Reference](https://developer.dataiku.com/latest/api-reference/python/client.html)
