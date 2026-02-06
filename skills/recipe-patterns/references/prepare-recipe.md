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
# PrepareRecipeSettings uses `raw_steps` property (NOT get_recipe_raw_params which does not exist)
settings = recipe.get_settings()

# Add steps via raw_steps (returns a reference to the list)
settings.raw_steps.append({
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "revenue",
        "expression": "price * quantity"
    }
})

settings.save()

# Apply schema updates and run
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()

job = recipe.run(no_fail=True)
```

## Common Prepare Processors

| Processor Type | Purpose |
|----------------|---------|
| `CreateColumnWithGREL` | Add formula column |
| `ColumnRenamer` | Rename columns |
| `FilterOnValue` | Filter rows |
| `ColumnsSelector` | Keep/remove columns |
| `FillEmptyWithValue` | Handle nulls |
