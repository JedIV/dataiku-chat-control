# Build Strategies

## Dependency Ordering

Dataiku flows are DAGs (directed acyclic graphs). When building via the API, you must respect the dependency order — upstream datasets must be built before downstream ones.

### Determine Build Order

```python
# List all recipes and their inputs/outputs to understand dependencies
recipes = project.list_recipes()
for r in recipes:
    print(f"{r['name']}:")
    for inp in r.get('inputs', {}).get('main', {}).get('items', []):
        print(f"  input: {inp['ref']}")
    for out in r.get('outputs', {}).get('main', {}).get('items', []):
        print(f"  output: {out['ref']}")
```

### Sequential Build Pattern

```python
# Define pipeline steps in dependency order
pipeline = [
    "step1_recipe",  # No dependencies
    "step2_recipe",  # Depends on step 1 output
    "step3_recipe",  # Depends on step 2 output
]

for recipe_name in pipeline:
    recipe = project.get_recipe(recipe_name)
    job = recipe.run(no_fail=True)
    state = job.get_status()["baseStatus"]["state"]

    if state != "DONE":
        print(f"Failed at {recipe_name}")
        break
```

## Idempotent Builds

Make scripts safe to re-run by checking for existing objects:

```python
existing_datasets = {d["name"] for d in project.list_datasets()}
existing_recipes = {r["name"] for r in project.list_recipes()}

def ensure_dataset(name, connection, schema_name):
    """Create dataset if it doesn't exist."""
    if name in existing_datasets:
        return project.get_dataset(name)

    builder = project.new_managed_dataset(name)
    builder.with_store_into(connection)
    ds = builder.create()

    settings = ds.get_settings()
    raw = settings.get_raw()
    raw["params"]["schema"] = schema_name
    raw["params"]["table"] = name
    settings.save()
    return ds


def ensure_recipe(recipe_type, recipe_name, inputs, output):
    """Create recipe if it doesn't exist."""
    if recipe_name in existing_recipes:
        return project.get_recipe(recipe_name)

    builder = project.new_recipe(recipe_type, recipe_name)
    for inp in inputs:
        builder.with_input(inp)
    builder.with_output(output)
    return builder.create()
```

## Dataset Status Checks

### Verify a Dataset Has Data

```python
ds = project.get_dataset("MY_DATASET")
schema = ds.get_settings().get_raw().get("schema", {}).get("columns", [])

if not schema:
    print("Dataset has no schema — may not be built yet")
else:
    print(f"Dataset has {len(schema)} columns")
```

### Get Dataset Metrics

```python
# Get computed metrics for a dataset (row count, etc.)
metrics = ds.get_last_metric_values()
values = metrics.get_global_value("records")
print(f"Row count: {values}")
```

## Error Recovery

When a pipeline step fails, you typically fix the issue and re-run from the failed step onward:

```python
def run_pipeline(project, pipeline, start_from=0):
    """Run pipeline steps, optionally starting from a specific step."""
    for i, recipe_name in enumerate(pipeline):
        if i < start_from:
            print(f"Skipping {recipe_name}")
            continue

        recipe = project.get_recipe(recipe_name)
        job = recipe.run(no_fail=True)
        state = job.get_status()["baseStatus"]["state"]

        if state != "DONE":
            print(f"Failed at step {i}: {recipe_name}")
            print(f"Fix the issue and re-run with start_from={i}")
            return False

    return True
```
