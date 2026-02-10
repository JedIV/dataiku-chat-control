# Meanings (Semantic Column Types)

Meanings are instance-level semantic types that can be assigned to dataset columns. They help with data discovery, validation, and documentation.

## Meaning Types

| Type | Use When | Key Parameter |
|------|----------|---------------|
| `DECLARATIVE` | Simple label, no validation | — |
| `VALUES_LIST` | Column should contain specific values | `values` |
| `VALUES_MAPPING` | Map raw values to display values | `mappings` |
| `PATTERN` | Column should match a regex pattern | `pattern` |

## Create Meanings

### Values List
```python
client.create_meaning(
    id="country_code",
    label="Country Code",
    type="VALUES_LIST",
    values=["US", "UK", "FR", "DE", "JP", "CA", "AU"],
    normalizationMode="EXACT",   # or "LOWERCASE", "NORMALIZED"
    detectable=True              # Auto-detect on new columns
)
```

Values can also include colors for UI display:
```python
client.create_meaning(
    id="status",
    label="Status",
    type="VALUES_LIST",
    values=[
        {"value": "active", "color": "#4CAF50"},
        {"value": "inactive", "color": "#F44336"},
        {"value": "pending", "color": "#FF9800"}
    ]
)
```

### Values Mapping
```python
client.create_meaning(
    id="gender_code",
    label="Gender Code",
    type="VALUES_MAPPING",
    mappings=[
        {"from": "M", "to": "Male"},
        {"from": "F", "to": "Female"},
        {"from": "O", "to": "Other"}
    ],
    normalizationMode="EXACT"
)
```

### Pattern
```python
client.create_meaning(
    id="email_address",
    label="Email Address",
    type="PATTERN",
    pattern=r"^[\w.-]+@[\w.-]+\.\w+$",
    detectable=True
)
```

### Declarative
```python
client.create_meaning(
    id="pii_data",
    label="PII Data",
    type="DECLARATIVE",
    description="Column contains personally identifiable information"
)
```

## Normalization Modes

| Mode | Behavior | Available For |
|------|----------|---------------|
| `EXACT` | Values must match exactly | VALUES_LIST, VALUES_MAPPING |
| `LOWERCASE` | Case-insensitive matching | VALUES_LIST, VALUES_MAPPING |
| `NORMALIZED` | Ignores case, accents, whitespace | VALUES_LIST, VALUES_MAPPING |

Note: `PATTERN` type does not support normalization modes.

## List Meanings
```python
meanings = client.list_meanings()
for m in meanings:
    print(f"{m['id']}: {m['label']} ({m['type']})")
```

## Update a Meaning
```python
meaning = client.get_meaning("country_code")
definition = meaning.get_definition()

# Modify the definition
definition["entries"].append({"value": "BR"})
definition["description"] = "ISO country codes"

meaning.set_definition(definition)
```

## Assign a Meaning to a Column
```python
# Assign a meaning to a dataset column
dataset = project.get_dataset("MY_DATASET")
schema = dataset.get_schema()
schema['columns'][2]['meaning'] = "my_meaning_id"
dataset.set_schema(schema)
```

## Detectable Meanings

When `detectable=True`, Dataiku will consider assigning the meaning automatically to columns set to "Auto-detect" during schema inference. This is useful for common patterns like email addresses, phone numbers, or country codes.
