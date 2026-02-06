# Python Recipe

Use for: Custom transformations not possible with visual recipes.

```python
# Create python recipe using builder pattern
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
