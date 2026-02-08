---
name: ml-training
description: "Use when training prediction models, extracting metrics, configuring algorithms, or deploying models"
---

# ML Model Training Patterns

Reference patterns for training and deploying ML models via the Dataiku Python API.

## Quick Start: Create and Train a Prediction Model

```python
# Create ML task
ml_task = project.create_prediction_ml_task(
    input_dataset="MY_DATASET",
    target_variable="target_column",
    prediction_type="BINARY_CLASSIFICATION",  # or REGRESSION, MULTICLASS
    ml_backend_type="PY_MEMORY",
    guess_policy="DEFAULT",
    wait_guess_complete=True
)

# Train models (waits for completion)
trained_ids = ml_task.train(session_name="My Training Session")

# Get metrics for each trained model
for model_id in trained_ids:
    details = ml_task.get_trained_model_details(model_id)
    metrics = details.get_performance_metrics()
    algo = details.get_modeling_settings()["algorithm"]
    print(f"Model: {algo}")
    print(f"  AUC: {metrics.get('auc')}")
    print(f"  Log Loss: {metrics.get('logLoss')}")
```

## Deploy Model to Flow

**Important:** Only deploy models when explicitly requested by the user. After training, show results and let the user decide. When deploying, confirm whether to create new or update existing.

### First-time deployment (creates new saved model)

```python
result = ml_task.deploy_to_flow(
    model_id=best_model_id,
    model_name="my_model",
    train_dataset="MY_DATASET"
)
# Returns: {"savedModelId": "...", "trainRecipeName": "..."}
```

### Update existing saved model (new version)

```python
saved_model = project.get_saved_model("my_model")
sm_id = saved_model.get_id()
ml_task.redeploy_to_flow(model_id=new_model_id, saved_model_id=sm_id)
```

## Access Existing ML Task

```python
analyses = project.list_analyses()
analysis = project.get_analysis(analyses[0]['analysisId'])
ml_tasks_info = analysis.list_ml_tasks()
ml_task = analysis.get_ml_task(ml_tasks_info['mlTasks'][0]['mlTaskId'])
model_ids = ml_task.get_trained_models_ids()
```

## References

- **Model metrics, get_performance_metrics(), common metrics table** — see [references/model-metrics.md](references/model-metrics.md)
- **Algorithm names (UPPERCASE), enable/disable, hyperparameters** — see [references/algorithm-config.md](references/algorithm-config.md)
- **Feature importance, rawImportance, dummy filtering** — see [references/feature-importance.md](references/feature-importance.md)
