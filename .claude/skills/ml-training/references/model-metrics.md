# Model Metrics Reference

## Accessing Metrics

Use `get_performance_metrics()` on a trained model details object. This returns a flat dict of metric names to values:

```python
for model_id in trained_ids:
    details = ml_task.get_trained_model_details(model_id)
    metrics = details.get_performance_metrics()
    algo = details.get_modeling_settings()["algorithm"]

    print(f"Model: {algo}")
    print(f"  AUC: {metrics.get('auc')}")
    print(f"  Log Loss: {metrics.get('logLoss')}")
    print(f"  Avg Precision: {metrics.get('averagePrecision')}")
```

## Other Accessor Methods

| Method | Returns |
|--------|---------|
| `details.get_performance_metrics()` | Dict of metric name → value |
| `details.get_modeling_settings()` | Algorithm config dict (has `"algorithm"` key) |
| `details.get_preprocessing_settings()` | Feature preprocessing config |
| `details.get_train_info()` | Timing data (startTime, endTime, etc.) |
| `details.get_actual_modeling_params()` | Resolved hyperparameters |

## Common Metrics

| Metric | Description |
|--------|-------------|
| `auc` | Area Under ROC Curve (0-1, higher is better) |
| `logLoss` | Log loss / cross-entropy (lower is better) |
| `averagePrecision` | Area under precision-recall curve |
| `lift` | Lift at optimal threshold |
| `calibrationLoss` | Calibration error (lower is better) |
| `precision` | Precision at optimal threshold |
| `recall` | Recall at optimal threshold |
| `f1` | F1 score at optimal threshold |

For K-Fold cross-test, most metrics also have a `std` variant (e.g., `aucstd`).

## Per-Threshold Data (Binary Classification)

To access threshold-dependent curves (precision, recall, F1 at each threshold):

```python
raw = details.get_raw()
per_cut = raw['perf']['perCutData']
thresholds = per_cut['cut']     # List of tested threshold values
f1_scores = per_cut['f1']       # F1 at each threshold
precision = per_cut['precision'] # Precision at each threshold
recall = per_cut['recall']       # Recall at each threshold
```

## Extracting Metrics for Comparison

```python
results = []
for model_id in trained_ids:
    details = ml_task.get_trained_model_details(model_id)
    metrics = details.get_performance_metrics()
    algo = details.get_modeling_settings()["algorithm"]
    results.append({
        'model_id': model_id,
        'algorithm': algo,
        'auc': metrics.get('auc'),
        'logLoss': metrics.get('logLoss'),
        'averagePrecision': metrics.get('averagePrecision'),
    })

# Sort by AUC descending
results.sort(key=lambda x: x['auc'] or 0, reverse=True)
best = results[0]
print(f"Best model: {best['algorithm']} (AUC={best['auc']:.4f})")
```

## Raw Access (Advanced)

For data not exposed by accessor methods, use `get_raw()`:

```python
raw = details.get_raw()
raw['perf']['tiMetrics']           # Same data as get_performance_metrics()
raw['trainInfo']['trainRows']      # Number of training samples
raw['trainInfo']['testRows']       # Number of test samples
raw['modeling']['algorithm']       # Algorithm name string
```
