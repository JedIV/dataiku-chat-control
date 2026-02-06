# Recipe Errors

## "Settings not saved"
Changes to recipe don't take effect.

**Cause:** Missing `settings.save()` call

**Solution:**
```python
settings = recipe.get_settings()
# ... make changes ...
settings.save()  # Don't forget this!
```

## "Recipe ran but no data"
Recipe completes but output is empty.

**Causes:**
- Filter removed all rows
- Join had no matches
- Input dataset is empty

**Solutions:**
1. Check input dataset row count
2. Verify join keys match (case-sensitive!)
3. Review filter conditions
4. Check job logs in Dataiku UI

## "Job failed"
```python
job.get_status()["baseStatus"]["state"] == "FAILED"
```

**Solutions:**
1. Get job logs:
   ```python
   log = job.get_log()
   print(log)
   ```
2. Check Dataiku UI for detailed errors
3. Common causes:
   - Schema mismatch
   - Missing input datasets
   - Resource limits exceeded

## Job API Usage

**Common Mistake:** Using non-existent methods
```python
# WRONG - wait_for_completion() doesn't exist on DSSJob
job = recipe.run()
job.wait_for_completion()  # AttributeError!
```

**Correct Pattern:**
```python
# recipe.run() already waits for completion internally
# Use no_fail=True to prevent exception on failure
job = recipe.run(no_fail=True)

# Job is already complete - check status
status = job.get_status()
state = status.get("baseStatus", {}).get("state")  # "DONE" or "FAILED"

if state == "FAILED":
    # Get error details from activities
    activities = status.get("baseStatus", {}).get("activities", {})
    for name, info in activities.items():
        if info.get("firstFailure"):
            print(f"Error: {info['firstFailure'].get('message')}")

    # Or get full log
    print(job.get_log())
```

## Join Issues

### Case Sensitivity
Joins are **case-sensitive**. "ABC" ≠ "abc"

**Solution:** Normalize keys before joining:
```python
# In prepare recipe, add processor:
{
    "type": "ColumnLowercaser",
    "params": {"columns": ["join_key"]}
}
```

### Type Mismatch
String "123" won't join with integer 123.

**Solution:** Cast columns to same type:
```python
# Convert to string
{
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "id_str",
        "expression": "toString(id)"
    }
}
```

## Schema Issues

### "Column not found"
```
Column 'x' not found in schema
```

**Causes:**
- Column renamed/removed
- Schema out of sync
- Case mismatch

**Solutions:**
1. List actual columns:
   ```python
   schema = dataset.get_settings().get_schema()
   print([c["name"] for c in schema["columns"]])
   ```
2. Update schema: `dataset.autodetect_settings()`

### Schema Mismatch After Recipe
Output schema doesn't match expected.

**Solution:**
```python
# Let Dataiku compute the correct schema
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()
```
