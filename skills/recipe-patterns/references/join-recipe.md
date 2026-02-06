# Join Recipe

Use for: Combining datasets on key columns.

## Basic Join (Two Datasets)

```python
# Create join recipe using the builder pattern
builder = project.new_recipe("join", "join_orders_customers")
builder.with_input("orders")       # Input 0 (left/base table)
builder.with_input("customers")    # Input 1 (right table)
builder.with_output("orders_enriched")
recipe = builder.create()

# Configure the join
settings = recipe.get_settings()

# Clear auto-generated joins (Dataiku guesses based on column names)
settings.raw_joins.clear()

# Add explicit join: orders LEFT JOIN customers ON ORDER_CUSTOMER_ID = CUSTOMER_ID
join = settings.add_join(join_type="LEFT", input1=0, input2=1)
settings.add_condition_to_join(join, type="EQ", column1="ORDER_CUSTOMER_ID", column2="CUSTOMER_ID")

settings.save()

# Apply schema updates to output dataset
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()
```

## Multi-Table Join with Column Selection

```python
# Join three tables: base LEFT JOIN table_a LEFT JOIN table_b
builder = project.new_recipe("join", "join_all_data")
builder.with_input("base_table")    # Input 0
builder.with_input("table_a")       # Input 1
builder.with_input("table_b")       # Input 2
builder.with_output("combined_data")
recipe = builder.create()

settings = recipe.get_settings()
settings.raw_joins.clear()

# Configure column selection on virtual inputs
virtual_inputs = settings.raw_virtual_inputs

# Input 1: Select specific columns only (exclude join key to avoid duplicates)
virtual_inputs[1]["columnsSelection"] = {
    "mode": "SELECT",
    "list": ["col_a1", "col_a2", "col_a3"]  # Only these columns from table_a
}

# Input 2: Select specific columns with prefix to avoid name conflicts
virtual_inputs[2]["columnsSelection"] = {
    "mode": "SELECT",
    "list": ["col_b1", "col_b2"]
}
virtual_inputs[2]["prefix"] = "tableb"  # Output: tableb_col_b1, tableb_col_b2 (Dataiku adds _ separator)

# Add joins
join1 = settings.add_join(join_type="LEFT", input1=0, input2=1)
settings.add_condition_to_join(join1, type="EQ", column1="ID", column2="BASE_ID")

join2 = settings.add_join(join_type="LEFT", input1=0, input2=2)
settings.add_condition_to_join(join2, type="EQ", column1="ID", column2="BASE_ID")

settings.save()

# Always apply schema updates after configuring joins
schema_updates = recipe.compute_schema_updates()
if schema_updates.any_action_required():
    schema_updates.apply()
```

## Join Types

| Type | Behavior |
|------|----------|
| `LEFT` | All rows from left table, matching rows from right (nulls if no match) |
| `INNER` | Only rows that match in both tables |
| `RIGHT` | All rows from right table, matching rows from left |
| `OUTER` | All rows from both tables |

## Column Selection Modes

| Mode | Behavior |
|------|----------|
| `SELECT` | Include only columns in `list` |
| `DROP` | Include all columns except those in `list` |

## Prefix Behavior

When using `prefix` on a virtual input, Dataiku adds its own `_` separator between the prefix and the column name. A prefix of `"tableb_"` produces output columns like `tableb__col_b1` (double underscore), not `tableb_col_b1`. To get single underscores, use a prefix without a trailing underscore (e.g., `"tableb"` produces `tableb_col_b1`).

Also note that `columnsSelection` with `mode: "DROP"` controls which columns are used in the join computation, but prefixed versions of dropped columns may still appear in the output. To reliably exclude columns (like duplicate join keys), use `mode: "SELECT"` and explicitly list only the columns you want.

**Warning**: Joins match column VALUES case-sensitively. Ensure join key values match exactly (e.g., "ABC" != "abc"). Use prepare recipes to normalize case before joining if needed.
