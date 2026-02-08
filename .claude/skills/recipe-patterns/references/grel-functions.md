# GREL Functions Reference

GREL (General Refine Expression Language) is used inside `CreateColumnWithGREL` and `FilterOnFormula` processors.

## Function Table

| Function | Example | Result |
|----------|---------|--------|
| `+`, `-`, `*`, `/` | `price * 1.1` | Math operations |
| `if(cond, then, else)` | `if(x > 0, 'pos', 'neg')` | Conditional (nestable) |
| `toString(val)` | `toString(123)` | `"123"` |
| `toNumber(val)` | `toNumber("123")` | `123` |
| `length(str)` | `length("abc")` | `3` |
| `trim(str)` | `trim(" x ")` | `"x"` |
| `upper(str)` | `upper("abc")` | `"ABC"` |
| `lower(str)` | `lower("ABC")` | `"abc"` |
| `datePart(date, part)` | `datePart(d, 'month')` | `1`-`12` |
| `isBlank(val)` | `isBlank("")` | `true` |
| `isNotBlank(val)` | `isNotBlank("x")` | `true` |
| `coalesce(a, b)` | `coalesce(null, 'default')` | `"default"` |

## Formula Syntax

### Arithmetic
Standard operators work on numeric columns.
```
price * quantity
(price * quantity) * (1 - discount / 100)
```

### String Concatenation
Use `+` to join strings.
```
first_name + ' ' + last_name
street + ', ' + city + ', ' + state + ' ' + zip
```

### Conditional Logic
`if(condition, value_if_true, value_if_false)` -- nestable for multi-branch:
```
if(amount > 1000, 'large', if(amount > 100, 'medium', 'small'))
```

### Boolean Operators
Use `&&` (AND) and `||` (OR) in filter formulas:
```
amount > 0 && isNotBlank(customer_id)
status == 'active' || status == 'pending'
```

### Date Extraction
`datePart(column, part)` extracts a component from a date column.

Valid parts: `year`, `month`, `day`, `hour`, `minute`, `second`, `dayOfWeek`.
```
datePart(order_date, 'year')
datePart(order_date, 'month')
datePart(order_date, 'dayOfWeek')
```

### Null Handling
```
coalesce(preferred_name, first_name)   -- first non-null wins
isBlank(email)                          -- true if null or empty
isNotBlank(customer_id)                 -- true if has a value
```

## Usage in Processors

### Calculated Column
```python
{
    "type": "CreateColumnWithGREL",
    "params": {
        "column": "revenue",
        "expression": "price * quantity"
    }
}
```

### Filter by Formula
```python
{
    "type": "FilterOnFormula",
    "params": {
        "formula": "amount > 0 && isNotBlank(customer_id)",
        "action": "KEEP"
    }
}
```
