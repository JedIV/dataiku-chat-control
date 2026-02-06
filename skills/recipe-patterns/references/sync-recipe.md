# Sync Recipe

Use for: Copying data between connections (e.g., to a data warehouse).

```python
# Create sync recipe using builder pattern
builder = project.new_recipe("sync", "sync_to_warehouse")
builder.with_input("final_output")
builder.with_output("warehouse_table")
recipe = builder.create()

settings = recipe.get_settings()
settings.save()

job = recipe.run(no_fail=True)
```
