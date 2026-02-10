# Algorithm Configuration Reference

## Configure Algorithms

Use the typed API methods on `DSSMLTaskSettings` / `DSSPredictionMLTaskSettings`:

- `settings.set_algorithm_enabled(name, True/False)` — enable or disable by name
- `settings.get_algorithm_settings(name)` — get settings dict for an algorithm
- `settings.disable_all_algorithms()` — disable everything at once
- `settings.get_all_possible_algorithm_names()` — list all valid algorithm names

Algorithm names are **UPPERCASE** strings.

```python
settings = ml_task.get_settings()

# Disable all, then enable specific ones
settings.disable_all_algorithms()
settings.set_algorithm_enabled("XGBOOST_CLASSIFICATION", True)
settings.set_algorithm_enabled("RANDOM_FOREST_CLASSIFICATION", True)

settings.save()
```

## Common Algorithm Names

| Algorithm | Classification Name | Regression Name |
|-----------|-------------------|----------------|
| Random Forest | `RANDOM_FOREST_CLASSIFICATION` | `RANDOM_FOREST_REGRESSION` |
| XGBoost | `XGBOOST_CLASSIFICATION` | `XGBOOST_REGRESSION` |
| Logistic Regression | `LOGISTIC_REGRESSION` | — |
| Gradient Boosted Trees | `GBT_CLASSIFICATION` | `GBT_REGRESSION` |
| LightGBM | `LIGHTGBM_CLASSIFICATION` | `LIGHTGBM_REGRESSION` |
| Neural Network | `NEURAL_NETWORK` | `NEURAL_NETWORK` |
| Decision Tree | `DECISION_TREE_CLASSIFICATION` | `DECISION_TREE_REGRESSION` |

Other available names: `EXTRA_TREES`, `KNN`, `LASSO_REGRESSION`, `RIDGE_REGRESSION`, `SGD_CLASSIFICATION`, `SGD_REGRESSION`, `SVC_CLASSIFICATION`, `SVM_REGRESSION`, `LARS`, `LEASTSQUARE_REGRESSION`.

Use `settings.get_all_possible_algorithm_names()` to see the full list for your environment.

## Enable a Single Algorithm

```python
settings = ml_task.get_settings()
settings.disable_all_algorithms()
settings.set_algorithm_enabled("XGBOOST_CLASSIFICATION", True)
settings.save()
```

## Enable Multiple Algorithms

```python
desired = ["XGBOOST_CLASSIFICATION", "RANDOM_FOREST_CLASSIFICATION", "LOGISTIC_REGRESSION"]

settings = ml_task.get_settings()
settings.disable_all_algorithms()
for algo in desired:
    settings.set_algorithm_enabled(algo, True)
settings.save()
```

## Tune Hyperparameters

`get_algorithm_settings(name)` returns a dict-like object with hyperparameter keys. Modify and save:

```python
settings = ml_task.get_settings()
xgb = settings.get_algorithm_settings("XGBOOST_CLASSIFICATION")
xgb["enabled"] = True
xgb["max_depth"] = 6
xgb["n_estimators"] = 300
settings.save()
```
