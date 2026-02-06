---
name: recipe-patterns
description: "Use when creating, configuring, or running any Dataiku recipe (prepare, join, group, sync, python) including data cleaning, formulas, and GREL"
---

# Dataiku Recipe Patterns

Reference patterns for creating different recipe types via the Python API.

## Recipe Type Decision Table

| Recipe Type | Use When | Key Method |
|-------------|----------|------------|
| **Prepare** | Column transforms, filtering, formula columns, renaming, data cleaning | `project.new_recipe("prepare", ...)` |
| **Join** | Combining datasets on key columns (LEFT, INNER, RIGHT, OUTER) | `project.new_recipe("join", ...)` |
| **Group** | Aggregations: sum, count, avg, min, max, stddev, etc. | `project.new_recipe("grouping", ...)` |
| **Sync** | Copying data between connections (e.g., to a data warehouse) | `project.new_recipe("sync", ...)` |
| **Python** | Custom transformations not possible with visual recipes | `project.new_recipe("python", ...)` |

## Universal Builder Pattern

Every recipe follows the same create-configure-run lifecycle:

```python
# 1. Create via builder
builder = project.new_recipe("<type>", "<recipe_name>")
builder.with_input("<input_dataset>")
builder.with_output("<output_dataset>")
recipe = builder.create()

# 2. Configure settings
settings = recipe.get_settings()
# ... recipe-specific configuration ...
settings.save()

# 3. Apply schema updates (visual recipes only)
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()

# 4. Run and check
job = recipe.run(no_fail=True)
state = job.get_status()["baseStatus"]["state"]  # "DONE" or "FAILED"
```

## Prepare Recipe Quick Reference

Prepare recipes use `raw_steps` to add processors:

```python
settings = recipe.get_settings()
settings.raw_steps.append({
    "type": "CreateColumnWithGREL",
    "params": {"column": "revenue", "expression": "price * quantity"}
})
settings.save()
```

### Common Processors

| Processor | Purpose |
|-----------|---------|
| `CreateColumnWithGREL` | Add calculated / derived columns |
| `ColumnTrimmer` | Strip whitespace from text columns |
| `ColumnLowercaser` | Lowercase text for consistency |
| `FillEmptyWithValue` | Replace nulls with a default |
| `FilterOnValue` | Keep or remove rows by column value |
| `FilterOnFormula` | Keep or remove rows by GREL expression |
| `ColumnRenamer` | Rename columns |
| `ColumnsSelector` | Keep or remove a set of columns |
| `ColumnSplitter` | Split a column by delimiter |
| `DateParser` | Parse string to date |
| `DateFormatter` | Format date to string |

### Top 5 GREL Patterns

| Pattern | Example | Notes |
|---------|---------|-------|
| Math | `price * quantity` | Standard operators `+`, `-`, `*`, `/` |
| Conditional | `if(amount > 1000, 'large', 'small')` | Nestable: `if(..., ..., if(...))` |
| String ops | `upper(name)`, `trim(val)`, `length(s)` | Also `lower()`, `toString()` |
| Date extraction | `datePart(order_date, 'month')` | Parts: `year`, `month`, `day`, `hour` |
| Coalesce | `coalesce(val, 'default')` | Returns first non-null argument |

## Always Remember

1. Call `settings.save()` after configuration changes
2. Call `compute_schema_updates().apply()` for visual recipes (join, grouping, etc.)
3. Call `recipe.run(no_fail=True)` to execute (already waits for completion)
4. Check `job.get_status()["baseStatus"]["state"]` for success ("DONE") or failure ("FAILED")
5. Verify output dataset has expected data and schema

## Common Pitfalls

### Schema Propagation
Visual recipes (join, grouping) need schema updates applied before running:
```python
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()
```

### Column Case for SQL Databases
Use UPPERCASE column names in dataset schemas to avoid "invalid identifier" errors:
```python
for col in raw["schema"]["columns"]:
    col["name"] = col["name"].upper()
```

### Job Completion
`recipe.run()` already waits -- do not look for `wait_for_completion()`:
```python
job = recipe.run(no_fail=True)  # Returns after job completes
state = job.get_status()["baseStatus"]["state"]  # "DONE" or "FAILED"
```

## Detailed References

**Recipe types:**
- [references/prepare-recipe.md](references/prepare-recipe.md) — Prepare recipe builder pattern, raw_steps API
- [references/join-recipe.md](references/join-recipe.md) — Join configuration, multi-table joins, column selection, prefix behavior
- [references/group-recipe.md](references/group-recipe.md) — Aggregation flags, output naming, type compatibility
- [references/sync-recipe.md](references/sync-recipe.md) — Sync recipe pattern
- [references/python-recipe.md](references/python-recipe.md) — Python recipe with `set_code`

**Data preparation:**
- [references/processors.md](references/processors.md) — All processor types with parameters and complete example
- [references/grel-functions.md](references/grel-functions.md) — Full GREL function table and formula syntax
- [references/date-operations.md](references/date-operations.md) — DateParser, DateFormatter, datePart examples

## Working Examples

- [scripts/run_recipe.py](../../scripts/run_recipe.py) — Run any recipe by name and check job status
