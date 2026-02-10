# Prepare Recipe

Use for: Column transformations, filtering, formula columns, renaming.

## Builder Pattern

```python
# Create prepare recipe using builder pattern
builder = project.new_recipe("prepare", "prepare_mydata")
builder.with_input("source_dataset")
builder.with_output("prepared_dataset")
recipe = builder.create()

# Get settings and add processors
settings = recipe.get_settings()

# Preferred: use add_processor_step() — the official API method
settings.add_processor_step("CreateColumnWithGREL", {
    "column": "revenue",
    "expression": "price * quantity"
})

settings.save()

# Alternative: raw_steps.append() for direct dict manipulation
# settings.raw_steps.append({
#     "type": "CreateColumnWithGREL",
#     "params": {
#         "column": "revenue",
#         "expression": "price * quantity"
#     }
# })

# Apply schema updates and run
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()

job = recipe.run(no_fail=True)
```

## add_processor_step() Examples

`add_processor_step(type, params)` is the preferred way to add processors. The `params` dict
is passed directly (without a wrapping `"params"` key):

```python
settings = recipe.get_settings()

# Filter rows where a column is not a valid type
settings.add_processor_step("FilterOnBadType", {
    "action": "REMOVE_ROW",
    "booleanMode": "AND",
    "appliesTo": "SINGLE_COLUMN",
    "columns": ["my_column"],
    "type": "Double"
})

# Rename a column
settings.add_processor_step("ColumnRenamer", {
    "renamings": [{"from": "old_name", "to": "new_name"}]
})

# Fill empty values
settings.add_processor_step("FillEmptyWithValue", {
    "appliesTo": "SINGLE_COLUMN",
    "columns": ["my_column"],
    "value": "N/A"
})

settings.save()
```

> **Note:** `raw_steps.append()` still works for direct dict manipulation (wrap params under
> a `"params"` key), but `add_processor_step()` is the official API method and should be preferred.

## Common Prepare Processors

| Processor Type | Purpose |
|----------------|---------|
| `CreateColumnWithGREL` | Add formula column |
| `ColumnRenamer` | Rename columns |
| `FilterOnValue` | Filter rows |
| `ColumnsSelector` | Keep/remove columns |
| `FillEmptyWithValue` | Handle nulls |
