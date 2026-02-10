# Group Recipe

Use for: Aggregations (sum, count, avg, etc.)

## Basic Grouping

```python
# Create grouping recipe using builder pattern
builder = project.new_recipe("grouping", "group_by_category")
builder.with_input("sales_data")
builder.with_output("category_summary")
builder.with_group_key("CATEGORY")  # Column to group by
recipe = builder.create()

# Configure aggregations
settings = recipe.get_settings()

# Enable global count (counts rows per group)
settings.set_global_count_enabled(True)

# Set aggregations per column using the typed API
settings.set_column_aggregations("AMOUNT", type="double", sum=True, avg=True, min=True, max=True)
settings.set_column_aggregations("CUSTOMER_ID", type="string", count_distinct=True)

settings.save()

# Apply schema updates to output dataset
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()
```

## set_column_aggregations() Reference

```python
settings.set_column_aggregations(
    column,             # Column name (required)
    type=None,          # Column type: "double", "string", "bigint", etc.
    min=False,
    max=False,
    count=False,
    count_distinct=False,
    sum=False,
    concat=False,
    stddev=False,
    avg=False
)
```

Returns a dict reference to the column settings. You can modify it for advanced options:

```python
col_settings = settings.set_column_aggregations("STATUS", type="string", concat=True)
col_settings["concatDistinct"] = True
col_settings["concatSeparator"] = ", "
settings.save()
```

## Output Column Naming Convention

Grouping recipes produce output columns with specific names:

| Aggregation | Output Column Name |
|-------------|-------------------|
| Global count | `count` |
| Column sum | `{COLUMN}_sum` |
| Column avg | `{COLUMN}_avg` |
| Column min | `{COLUMN}_min` |
| Column max | `{COLUMN}_max` |
| Column count | `{COLUMN}_count` |
| Column count distinct | `{COLUMN}_distinct` |
| Column stddev | `{COLUMN}_std` |
| Column concat | `{COLUMN}_concat` |

**Important**: Note that `countDistinct` in the API produces `_distinct` suffix (not `_countDistinct`).

## Available Aggregations

The `set_column_aggregations()` method supports: `min`, `max`, `count`, `count_distinct`, `sum`, `concat`, `stddev`, `avg`.

For `first`, `last`, `concatDistinct`, and `concatSeparator`, use the raw payload approach:

```python
# For aggregations not in set_column_aggregations, use the raw payload
payload = settings.get_json_payload()
payload["values"].append({
    "column": "MY_COLUMN",
    "type": "double",
    "first": True,
    "last": True,
    "orderColumn": "EVENT_DATE"  # Required for first/last
})
settings.set_json_payload(payload)
settings.save()
```

## Type Compatibility for Aggregations

Not all aggregations work on all column types. Using an incompatible aggregation causes a runtime error (e.g., `Cannot avg non-numeric column`).

| Aggregation | Numeric (double, bigint) | String | Date |
|-------------|:---:|:---:|:---:|
| `sum` | Yes | **No** | **No** |
| `avg` | Yes | **No** | **No** |
| `stddev` | Yes | **No** | **No** |
| `min` / `max` | Yes | Yes | Yes |
| `count` / `countDistinct` | Yes | Yes | Yes |
| `first` / `last` | Yes | Yes | Yes |
| `concat` / `concatDistinct` | Yes | Yes | Yes |

## `first` and `last` Require `orderColumn`

The `first` and `last` aggregations require an `orderColumn` parameter to determine row ordering. Without it, the recipe fails with: `orderColumn parameter is required for FIRST aggregation`.

```python
payload["values"].append({
    "column": "STATUS",
    "type": "string",
    "last": True,
    "orderColumn": "EVENT_DATE"  # Required: which column determines first/last
})
```

If you just need the earliest or latest value of a date/string column, use `min` and `max` instead -- they do not require `orderColumn`.

## Schema Propagation

Always let Dataiku compute the output schema after configuring aggregations:

```python
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()
```

This ensures the output dataset schema matches what the recipe will actually produce.
