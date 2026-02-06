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

# Clear default aggregations and set specific ones
payload = settings.get_json_payload()
payload["values"] = []

# Add aggregations - each produces an output column
payload["values"].append({
    "column": "AMOUNT",
    "type": "double",
    "sum": True,      # Output: AMOUNT_sum
    "avg": True,      # Output: AMOUNT_avg
    "min": True,      # Output: AMOUNT_min
    "max": True       # Output: AMOUNT_max
})

payload["values"].append({
    "column": "CUSTOMER_ID",
    "type": "string",
    "countDistinct": True  # Output: CUSTOMER_ID_distinct
})

settings.set_json_payload(payload)
settings.save()

# Apply schema updates to output dataset
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()
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

## Available Aggregation Flags

```python
{
    "column": "MY_COLUMN",
    "type": "double",  # or "string", "bigint", etc.
    "sum": True,
    "avg": True,
    "min": True,
    "max": True,
    "count": True,         # Count non-null values
    "countDistinct": True, # Count unique values
    "stddev": True,
    "first": True,
    "last": True,
    "concat": True,        # Concatenate string values
    "concatDistinct": True
}
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
