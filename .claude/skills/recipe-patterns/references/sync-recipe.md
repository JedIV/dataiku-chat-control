# Sync Recipe

Use for: Copying data between connections (e.g., to a data warehouse).

## Creating with a new output dataset (preferred)

Use `with_new_output` to create the output dataset automatically as part of recipe creation — no need to create the dataset separately first.

```python
builder = project.new_recipe("sync", "sync_to_warehouse")
builder.with_input("source_dataset")
builder.with_new_output("target_dataset", "connection_name")
recipe = builder.create()

settings = recipe.get_settings()
settings.save()

job = recipe.run(no_fail=True)
```

## Using an existing output dataset

Use `with_output` when the output dataset already exists.

```python
builder = project.new_recipe("sync", "sync_to_warehouse")
builder.with_input("source_dataset")
builder.with_output("existing_target_dataset")
recipe = builder.create()

settings = recipe.get_settings()
settings.save()

job = recipe.run(no_fail=True)
```
