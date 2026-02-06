# Feature Importance Reference

## rawImportance Structure

For tree-based models (Random Forest, XGBoost, GBT, LightGBM, Decision Tree), feature importance is stored in `iperf.rawImportance` as **parallel arrays**:

```python
raw['iperf']['rawImportance']
# {
#     'variables': ['feature1', 'feature2', 'dummy:category:value1', ...],
#     'importances': [0.5, 0.2, 0.05, ...]
# }
```

- `variables` — list of feature names (includes dummy-encoded columns)
- `importances` — list of importance values (same length, same order as variables)

## Extract and Sort Feature Importance

```python
details = ml_task.get_trained_model_details(model_id)
raw = details.get_raw()

# For tree-based models: rawImportance contains parallel arrays
raw_importance = raw.get('iperf', {}).get('rawImportance', {})
variables = raw_importance.get('variables', [])    # List of feature names
importances = raw_importance.get('importances', []) # List of importance values

# Combine and sort
feat_imp = list(zip(variables, importances))
sorted_imp = sorted(feat_imp, key=lambda x: x[1], reverse=True)

for feat, imp in sorted_imp[:10]:
    print(f"{feat}: {imp:.4f}")
```

## Filtering Dummy Variables

Dataiku creates one-hot encoded features prefixed with `dummy:` and cyclical datetime features prefixed with `datetime_cyclical:`. To see only original features:

```python
for feat, imp in sorted_imp:
    if not feat.startswith('dummy:') and not feat.startswith('datetime_cyclical:'):
        print(f"{feat}: {imp:.4f}")
```

## Feature Importance Structure Reference

The `get_raw()` dict contains these key sections for feature importance (not documented in API reference):

```python
raw = details.get_raw()

# Feature importance (tree-based models)
raw['iperf']['rawImportance']['variables']    # ['feature1', 'feature2', ...]
raw['iperf']['rawImportance']['importances']  # [0.5, 0.2, ...]
```

## Access Existing ML Task to Get Feature Importance

```python
# List analyses in project
analyses = project.list_analyses()

# Get analysis and ML task
analysis = project.get_analysis(analyses[0]['analysisId'])
ml_tasks_info = analysis.list_ml_tasks()
ml_task = analysis.get_ml_task(ml_tasks_info['mlTasks'][0]['mlTaskId'])

# Get all trained models
model_ids = ml_task.get_trained_models_ids()

# Get feature importance for each model
for model_id in model_ids:
    details = ml_task.get_trained_model_details(model_id)
    raw = details.get_raw()
    algo = raw['modeling']['algorithm']

    raw_importance = raw.get('iperf', {}).get('rawImportance', {})
    variables = raw_importance.get('variables', [])
    importances = raw_importance.get('importances', [])

    if variables:
        feat_imp = sorted(zip(variables, importances), key=lambda x: x[1], reverse=True)
        print(f"\n{algo} — Top 10 features:")
        for feat, imp in feat_imp[:10]:
            if not feat.startswith('dummy:'):
                print(f"  {feat}: {imp:.4f}")
```
