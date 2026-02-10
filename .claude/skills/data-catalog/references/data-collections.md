# Data Collections

## Overview

Data collections are instance-level groups of datasets that span across projects. They are managed via `client` (not `project`), and datasets from any project can be added.

## Full API

### Create
```python
dc = client.create_data_collection(
    displayName="My Collection",
    id=None,              # Auto-generated 8-char ID if omitted
    tags=["tag1"],
    description="Description text",
    color="#540d6e",       # #RRGGBB format, random if omitted
    permissions=[          # Current user always added as admin
        {"user": "alice@example.com", "admin": False, "write": True, "read": True}
    ]
)
```

### List
```python
# As list items (default) — lightweight, has item_count and last_modified_on
items = client.list_data_collections(as_type="listitems")
for item in items:
    print(f"{item.display_name} — {item.item_count} items")
    dc = item.to_data_collection()  # Convert to full handle

# As dicts — raw data
dicts = client.list_data_collections(as_type="dict")

# As full objects
objects = client.list_data_collections(as_type="objects")
```

### Add Objects
```python
dc = client.get_data_collection("collection_id")

# From a dataset handle
ds = project.get_dataset("MY_DATASET")
dc.add_object(ds)

# From a dict (useful for cross-project)
dc.add_object({
    "type": "DATASET",
    "projectKey": "OTHER_PROJECT",
    "id": "THEIR_DATASET"
})
```

### List Objects
```python
# As DSSDataCollectionItem objects (default)
items = dc.list_objects()  # as_type="objects" is the default
for item in items:
    raw = item.get_raw()  # {"type": "DATASET", "projectKey": "...", "id": "..."}
    ds = item.get_as_dataset()  # Get DSSDataset handle

# As dicts
dicts = dc.list_objects(as_type="dict")
```

### Remove Objects
```python
items = dc.list_objects(as_type="objects")  # Must use "objects" for .get_raw() and .remove()
for item in items:
    if item.get_raw()["id"] == "UNWANTED_DATASET":
        item.remove()
```

### Settings and Permissions
```python
settings = dc.get_settings()

# Read properties
print(settings.id)            # Read-only
print(settings.display_name)
print(settings.description)
print(settings.color)
print(settings.tags)
print(settings.permissions)   # None if you're not an admin

# Modify properties
settings.display_name = "New Name"
settings.description = "New description"
settings.color = "#2196F3"
settings.tags = ["updated", "production"]
settings.permissions = [
    {"user": "alice@example.com", "admin": True, "write": True, "read": True},
    {"group": "data-team", "admin": False, "write": True, "read": True}
]
settings.save()  # Requires admin rights
```

There is also a `DSSDataCollectionPermissionItem` helper class with static builder methods for constructing permission entries:
```python
from dataikuapi.dss.data_collection import DSSDataCollectionPermissionItem

settings.permissions = [
    DSSDataCollectionPermissionItem.admin_user("alice@example.com"),
    DSSDataCollectionPermissionItem.contributor_group("data-team"),
    DSSDataCollectionPermissionItem.reader_user("bob@example.com"),
]
settings.save()
```

### Metadata Completeness Checks

The raw settings include `metadataCompletenessChecks` which controls whether the collection enforces descriptions:

```python
raw = settings.get_raw()
raw["metadataCompletenessChecks"] = {
    "longDescriptionCheck": "ENABLED",      # or "DISABLED"
    "columnsDescriptionCheck": "ENABLED"
}
settings.save()
```

### Delete
```python
dc.delete()  # Requires admin rights on the collection
```
