# Python Recipe

Use for: Custom transformations not possible with visual recipes.

## With Existing Output Dataset

```python
# Create python recipe with an existing output dataset
builder = project.new_recipe("python", "custom_transform")
builder.with_input("input_data")
builder.with_output("output_data")
recipe = builder.create()

settings = recipe.get_settings()
settings.set_code('''
import dataiku
import pandas as pd

input_df = dataiku.Dataset("input_data").get_dataframe()

# Your custom logic here
output_df = input_df.copy()

dataiku.Dataset("output_data").write_with_schema(output_df)
''')

settings.save()

job = recipe.run(no_fail=True)
```

## With New Output Dataset

Use `with_new_output_dataset()` to create the output dataset as part of recipe creation.
Note: the method is `with_new_output_dataset()`, NOT `with_new_output()`.

```python
# Create python recipe and its output dataset in one step
builder = project.new_recipe("python", "my_python_recipe")
builder.with_input("input_dataset")
builder.with_new_output_dataset("output_dataset", "connection_name")
builder.with_script("""
import dataiku
input_ds = dataiku.Dataset("input_dataset")
output_ds = dataiku.Dataset("output_dataset")
df = input_ds.get_dataframe()
# ... transform ...
output_ds.write_with_schema(df)
""")
recipe = builder.create()
```
