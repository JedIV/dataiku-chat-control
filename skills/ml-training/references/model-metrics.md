# Model Metrics Reference

## Accessing Metrics

For binary classification, metrics are in `raw['perf']['tiMetrics']`:

```python
for model_id in trained_ids:
    details = ml_task.get_trained_model_details(model_id)
    raw = details.get_raw()

    algo = raw['modeling']['algorithm']
    metrics = raw['perf']['tiMetrics']

    print(f"Model: {algo}")
    print(f"  AUC: {metrics.get('auc')}")
    print(f"  Log Loss: {metrics.get('logLoss')}")
    print(f"  Avg Precision: {metrics.get('averagePrecision')}")
```

> **CRITICAL:** Metrics are NOT in `trainInfo.testPerf` or `globalMetrics` as you might expect. Always use `perf.tiMetrics` for classification metrics.

## tiMetrics Structure

The `tiMetrics` dict is a flat dictionary of metric name to numeric value:

```python
raw['perf']['tiMetrics']
# {
#     'auc': 0.85,
#     'logLoss': 0.4,
#     'averagePrecision': 0.9,
#     'lift': 2.3,
#     'calibrationLoss': 0.02,
#     ...
# }
```

## Common Metrics in tiMetrics

| Metric | Description |
|--------|-------------|
| `auc` | Area Under ROC Curve (0-1, higher is better) |
| `logLoss` | Log loss / cross-entropy (lower is better) |
| `averagePrecision` | Area under precision-recall curve |
| `lift` | Lift at optimal threshold |
| `calibrationLoss` | Calibration error (lower is better) |

## Full get_raw() Performance Structure

The `get_raw()` dict contains these key sections (not documented in API reference):

```python
raw = details.get_raw()

# Model performance metrics
raw['perf']['tiMetrics']  # {'auc': 0.85, 'logLoss': 0.4, 'averagePrecision': 0.9, ...}

# Training info
raw['trainInfo']['trainRows']      # Number of training samples
raw['trainInfo']['testRows']       # Number of test samples

# Model configuration
raw['modeling']['algorithm']       # 'RANDOM_FOREST_CLASSIFICATION', etc.
```

## Extracting Metrics for Comparison

```python
results = []
for model_id in trained_ids:
    details = ml_task.get_trained_model_details(model_id)
    raw = details.get_raw()
    results.append({
        'model_id': model_id,
        'algorithm': raw['modeling']['algorithm'],
        'auc': raw['perf']['tiMetrics'].get('auc'),
        'logLoss': raw['perf']['tiMetrics'].get('logLoss'),
        'averagePrecision': raw['perf']['tiMetrics'].get('averagePrecision'),
    })

# Sort by AUC descending
results.sort(key=lambda x: x['auc'] or 0, reverse=True)
best = results[0]
print(f"Best model: {best['algorithm']} (AUC={best['auc']:.4f})")
```
