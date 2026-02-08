# Prepare Recipe Processors

Complete reference for all processor types used in Dataiku prepare recipes.

## Common Cleaning Processors

```python
import dataikuapi, os

client = dataikuapi.DSSClient(os.environ["DSS_URL"], os.environ["DSS_API_KEY"])
project = client.get_project(os.environ["DSS_PROJECT_KEY"])

# Create recipe via builder pattern
builder = project.new_recipe("prepare", "clean_data")
builder.with_input("raw_data")
builder.with_output("clean_data")
recipe = builder.create()

settings = recipe.get_settings()

# Trim whitespace from text columns
settings.raw_steps.append({
    "type": "ColumnTrimmer",
    "params": {"columns": ["name", "address"]}
})

# Lowercase for consistency
settings.raw_steps.append({
    "type": "ColumnLowercaser",
    "params": {"columns": ["email"]}
})

# Remove duplicates
settings.raw_steps.append({
    "type": "RemoveDuplicates",
    "params": {"columns": ["id"]}
})

# Fill nulls with default
settings.raw_steps.append({
    "type": "FillEmptyWithValue",
    "params": {"column": "status", "value": "unknown"}
})

settings.save()
```

## CreateColumnWithGREL

Add calculated or derived columns using GREL expressions.

```python
# Add revenue column
{
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "revenue",
        "expression": "price * quantity"
    }
}

# String concatenation
{
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "full_name",
        "expression": "first_name + ' ' + last_name"
    }
}

# Conditional logic
{
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "size_category",
        "expression": "if(amount > 1000, 'large', if(amount > 100, 'medium', 'small'))"
    }
}

# Date extraction
{
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "year",
        "expression": "datePart(order_date, 'year')"
    }
}

# Merge columns
{
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "address_full",
        "expression": "street + ', ' + city + ', ' + state + ' ' + zip"
    }
}
```

## FilterOnValue

Keep or remove rows matching specific column values.

```python
{
    "type": "FilterOnValue",
    "params": {
        "column": "status",
        "values": ["active", "pending"],
        "action": "KEEP"  # or "REMOVE"
    }
}
```

## FilterOnFormula

Keep or remove rows using a GREL boolean expression.

```python
# Filter by formula
{
    "type": "FilterOnFormula",
    "params": {
        "formula": "amount > 0 && isNotBlank(customer_id)",
        "action": "KEEP"
    }
}

# Filter by date range
{
    "type": "FilterOnFormula",
    "params": {
        "formula": "order_date >= '2024-01-01' && order_date < '2025-01-01'",
        "action": "KEEP"
    }
}
```

## ColumnRenamer

Rename one or more columns.

```python
{
    "type": "ColumnRenamer",
    "params": {
        "renamings": [
            {"from": "old_name", "to": "new_name"}
        ]
    }
}
```

## ColumnsSelector

Keep or remove a set of columns.

```python
# Keep only specific columns (in order)
{
    "type": "ColumnsSelector",
    "params": {
        "columns": ["id", "name", "amount", "date"],
        "keep": True
    }
}

# Remove columns
{
    "type": "ColumnsSelector",
    "params": {
        "columns": ["temp_col", "debug_col"],
        "keep": False
    }
}
```

## ColumnSplitter

Split a column by delimiter into new columns.

```python
{
    "type": "ColumnSplitter",
    "params": {
        "column": "full_name",
        "separator": " ",
        "outColumns": ["first_name", "last_name"]
    }
}
```

## Complete Example: Sales Data Prep

End-to-end example creating a prepare recipe that cleans, enriches, filters, and selects columns from a raw sales dataset.

```python
import dataikuapi
import os

client = dataikuapi.DSSClient(os.environ["DSS_URL"], os.environ["DSS_API_KEY"])
project = client.get_project(os.environ["DSS_PROJECT_KEY"])

# Create prepare recipe via builder pattern
builder = project.new_recipe("prepare", "prepare_sales")
builder.with_input("raw_sales")
builder.with_output("clean_sales")
recipe = builder.create()

settings = recipe.get_settings()

# Clean text fields
settings.raw_steps.append({
    "type": "ColumnTrimmer",
    "params": {"columns": ["customer_name", "product"]}
})

# Standardize case
settings.raw_steps.append({
    "type": "ColumnLowercaser",
    "params": {"columns": ["email"]}
})

# Add calculated fields
settings.raw_steps.append({
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "revenue",
        "expression": "price * quantity"
    }
})
settings.raw_steps.append({
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "month",
        "expression": "datePart(order_date, 'month')"
    }
})

# Filter valid records
settings.raw_steps.append({
    "type": "FilterOnFormula",
    "params": {
        "formula": "quantity > 0 && isNotBlank(customer_id)",
        "action": "KEEP"
    }
})

# Keep only needed columns
settings.raw_steps.append({
    "type": "ColumnsSelector",
    "params": {
        "columns": ["order_id", "customer_id", "product", "revenue", "month", "order_date"],
        "keep": True
    }
})

settings.save()

# Run recipe (blocks until complete)
job = recipe.run(no_fail=True)
status = job.get_status()
state = status.get("baseStatus", {}).get("state")
print(f"Job completed with status: {state}")
```
