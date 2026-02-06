# Algorithm Configuration Reference

## Configure Algorithms

```python
settings = ml_task.get_settings()
raw = settings.get_raw()
modeling = raw['modeling']

# Disable all algorithms
for algo in modeling:
    if isinstance(modeling[algo], dict) and 'enabled' in modeling[algo]:
        modeling[algo]['enabled'] = False

# Enable specific ones
modeling['xgboost']['enabled'] = True
modeling['random_forest_classification']['enabled'] = True

settings.save()
```

## Common Algorithm Keys

| Algorithm | Classification Key | Regression Key |
|-----------|-------------------|----------------|
| Random Forest | `random_forest_classification` | `random_forest_regression` |
| XGBoost | `xgboost` | `xgboost` |
| Logistic Regression | `logistic_regression` | — |
| Gradient Boosted Trees | `gbt_classification` | `gbt_regression` |
| LightGBM | `lightgbm_classification` | `lightgbm_regression` |
| Neural Network | `neural_network` | `neural_network` |
| Decision Tree | `decision_tree_classification` | `decision_tree_regression` |

## Enable a Single Algorithm

```python
settings = ml_task.get_settings()
raw = settings.get_raw()
modeling = raw['modeling']

# Disable everything first
for algo in modeling:
    if isinstance(modeling[algo], dict) and 'enabled' in modeling[algo]:
        modeling[algo]['enabled'] = False

# Enable only XGBoost
modeling['xgboost']['enabled'] = True
settings.save()
```

## Enable Multiple Algorithms

```python
desired = ['xgboost', 'random_forest_classification', 'logistic_regression']

settings = ml_task.get_settings()
raw = settings.get_raw()
modeling = raw['modeling']

for algo in modeling:
    if isinstance(modeling[algo], dict) and 'enabled' in modeling[algo]:
        modeling[algo]['enabled'] = (algo in desired)

settings.save()
```
