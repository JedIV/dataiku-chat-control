# SQL Database Errors (Snowflake, BigQuery, etc.)

## "invalid identifier" with Quoted Column Name
```
SQL compilation error: invalid identifier '"my_column"'
```

**Cause:** Dataiku dataset schema has lowercase column names. When generating SQL, Dataiku quotes lowercase names, but the actual database column is uppercase (standard for SQL databases).

**Solution:** Normalize dataset schema to uppercase:
```python
ds = project.get_dataset("my_dataset")
settings = ds.get_settings()
raw = settings.get_raw()
for col in raw.get("schema", {}).get("columns", []):
    col["name"] = col["name"].upper()
settings.save()
```

**Prevention:** Always use uppercase column names in Dataiku schemas for SQL databases.

## "invalid identifier" (General)
```
SQL compilation error: invalid identifier 'TABLE.COLUMN'
```

**Causes:**
- Column doesn't exist in table
- Table alias mismatch
- Schema/catalog not specified

**Solutions:**
1. Verify column exists in source table
2. Check dataset's table configuration:
   ```python
   ds = project.get_dataset("my_dataset")
   params = ds.get_settings().get_raw().get("params", {})
   print(f"Table: {params.get('table')}")
   print(f"Schema: {params.get('schema')}")
   ```

## "table does not exist"
```
SQL compilation error: Table 'X' does not exist
```

**Causes:**
- Upstream dataset not built yet
- Wrong schema/catalog
- Table was dropped

**Solutions:**
1. Build upstream datasets first (respect dependency order)
2. Verify table configuration in dataset settings
3. Check database directly to confirm table exists

## Pre-Join Computed Columns Failing
When using SQL expressions in pre-join computed columns:

**Common Mistake:**
```python
# This may fail - Dataiku might quote the expression
settings.add_pre_join_computed_column(0, {
    "mode": "SQL",
    "expr": "UPPER(my_column)"  # May become UPPER("my_column")
})
```

**Solution:** Ensure column names in Dataiku schema match database (uppercase), or avoid computed columns and join directly on existing columns.

## "Insert value list does not match column list"
```
SQL compilation error: Insert value list does not match column list expecting N but got M
```

**Cause:** Output dataset schema doesn't match what recipe produces. Common with grouping recipes when aggregations change.

**Solution:**
```python
# After configuring recipe, always apply schema updates
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()
```
