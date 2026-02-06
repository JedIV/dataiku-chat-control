# Schema Operations Reference

Detailed code examples for all schema management operations in Dataiku.

## Get Dataset Schema

```python
dataset = project.get_dataset("my_dataset")
settings = dataset.get_settings()
schema = settings.get_schema()

# Schema is a list of column definitions
for col in schema["columns"]:
    print(f"{col['name']}: {col['type']}")
```

## Auto-detect Schema

For uploaded files, let Dataiku detect the schema:

```python
dataset = project.create_dataset(
    "new_dataset",
    type="UploadedFiles",
    params={"uploadConnection": "filesystem_managed"}
)

# Upload file
with open("data.csv", "rb") as f:
    dataset.uploaded_add_file(f, "data.csv")

# Auto-detect schema from file contents
dataset.autodetect_settings()

# Get and save the detected settings
settings = dataset.get_settings()
settings.save()
```

## Manually Set Schema

```python
dataset = project.get_dataset("my_dataset")
settings = dataset.get_settings()

# Define schema explicitly
new_schema = {
    "columns": [
        {"name": "id", "type": "string"},
        {"name": "amount", "type": "double"},
        {"name": "date", "type": "date"},
        {"name": "is_active", "type": "boolean"}
    ]
}

settings.set_schema(new_schema)
settings.save()
```

## Update Schema After Recipe

After running a recipe that changes columns:

```python
# Run recipe
job = recipe.run()
# Wait for completion...

# Update output dataset schema
output_ds = project.get_dataset("output_dataset")
output_ds.autodetect_settings()
output_settings = output_ds.get_settings()
output_settings.save()
```

## Schema Compatibility Check for Joins

Before creating a join, verify key columns match:

```python
def check_join_compatibility(project, ds1_name, ds2_name, key1, key2):
    """Check if join keys are compatible."""
    ds1 = project.get_dataset(ds1_name)
    ds2 = project.get_dataset(ds2_name)

    schema1 = ds1.get_settings().get_schema()
    schema2 = ds2.get_settings().get_schema()

    col1 = next((c for c in schema1["columns"] if c["name"] == key1), None)
    col2 = next((c for c in schema2["columns"] if c["name"] == key2), None)

    if not col1:
        print(f"Warning: {key1} not found in {ds1_name}")
        return False
    if not col2:
        print(f"Warning: {key2} not found in {ds2_name}")
        return False
    if col1["type"] != col2["type"]:
        print(f"Warning: Type mismatch - {key1}:{col1['type']} vs {key2}:{col2['type']}")
        return False

    return True
```

## List All Columns Helper

```python
def list_columns(project, dataset_name):
    """List all columns with types."""
    ds = project.get_dataset(dataset_name)
    schema = ds.get_settings().get_schema()

    print(f"Columns in {dataset_name}:")
    for col in schema["columns"]:
        print(f"  - {col['name']}: {col['type']}")

    return schema["columns"]
```
