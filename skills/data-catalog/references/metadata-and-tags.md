# Metadata and Tags

## Dataset Metadata

Every dataset has metadata accessible via `get_metadata()` / `set_metadata()`.

### Metadata Structure

```python
ds = project.get_dataset("MY_DATASET")
metadata = ds.get_metadata()

# Structure:
# {
#   "label": "Human-readable name",
#   "description": "Markdown description",
#   "tags": ["tag1", "tag2"],
#   "checklists": {
#     "checklists": [
#       {
#         "title": "Checklist name",
#         "items": [
#           {"done": false, "text": "Item text"}
#         ]
#       }
#     ]
#   },
#   "custom": {
#     "kv": {
#       "owner": "data-team",
#       "refresh_schedule": "daily"
#     }
#   }
# }
```

### Set Tags on a Dataset
```python
metadata = ds.get_metadata()
metadata["tags"] = ["production", "cleaned", "v2"]
ds.set_metadata(metadata)
```

### Set Custom Key-Value Metadata
```python
metadata = ds.get_metadata()
metadata["custom"]["kv"]["owner"] = "analytics-team"
metadata["custom"]["kv"]["source"] = "snowflake"
metadata["custom"]["kv"]["refresh"] = "daily"
ds.set_metadata(metadata)
```

### Set Description
```python
metadata = ds.get_metadata()
metadata["description"] = "Customer demographics from CRM export. Updated daily."
ds.set_metadata(metadata)
```

## Project Metadata

```python
project_meta = project.get_metadata()

# Structure:
# {
#   "label": "Project display name",
#   "shortDesc": "Short description",
#   "checklists": {...},
#   ...
# }

project_meta["shortDesc"] = "ML pipeline for loan default prediction"
project.set_metadata(project_meta)
```

## Project Tags

Project tags use a separate API from metadata tags:

```python
# Get tags
tags = project.get_tags()  # {"tags": {"tag_name": {}}}

# Set tags
project.set_tags({"tags": {
    "production": {},
    "ml": {},
    "v2": {}
}})
```

Note: Project tags are a dict of `{tag_name: {}}` (the value is always an empty dict). Dataset tags in metadata are a simple list of strings.

## AI-Generated Descriptions

Dataiku can auto-generate descriptions for datasets and their columns:

```python
# Generate without saving (preview)
result = ds.generate_ai_description(language="english", save_description=False)
print(result)

# Generate and save directly
ds.generate_ai_description(language="english", save_description=True)
```

### Supported Languages
`dutch`, `english`, `french`, `german`, `portuguese`, `spanish`

### Rate Limits
- 1000 requests per day per license
- After limit: each call takes ~60 seconds (throttled mode)
- Requires "Generate Metadata" enabled in AI Services admin settings
