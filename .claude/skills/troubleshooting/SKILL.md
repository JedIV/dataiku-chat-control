---
name: troubleshooting
description: "Use when debugging failed jobs, diagnosing errors, or resolving common Dataiku issues"
---

# Dataiku Troubleshooting Guide

## Debugging Checklist

1. [ ] Environment activated? `which python` should show dataiku-env
2. [ ] Variables set? `echo $DSS_URL`
3. [ ] Can connect? Run `scripts/bootstrap.py`
4. [ ] Recipe saved? Check for `settings.save()`
5. [ ] Job ran? Check for `recipe.run()`
6. [ ] Job succeeded? Check `job.get_status()`
7. [ ] Schema correct? Run `autodetect_settings()`

## Top-10 Error Quick Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | Wrong DSS_URL or instance down | Verify URL, check instance status |
| `401 Unauthorized` | Invalid or expired API key | Regenerate key in Dataiku UI |
| `Project not found` | Wrong project key or no access | `client.list_project_keys()` to verify |
| Settings not saved | Missing `settings.save()` | Always call `settings.save()` after changes |
| Recipe ran but no data | Filter/join removed all rows | Check inputs, join keys, filters |
| Job failed | Schema mismatch, missing inputs | Inspect job status and logs |
| `invalid identifier` (quoted) | Lowercase column names in SQL schema | Normalize schema to UPPERCASE |
| `table does not exist` | Upstream dataset not built | Build datasets in dependency order |
| `Insert value list mismatch` | Output schema doesn't match recipe output | Run `recipe.compute_schema_updates()` and apply |
| `ModuleNotFoundError: dataikuapi` | Virtual environment not activated | `source ~/dataiku-env/bin/activate` |

## Job Failure Investigation Pattern

```python
# Get the most recent job and extract error details
jobs = project.list_jobs()
job = project.get_job(jobs[0]['def']['id'])
status = job.get_status()
state = status.get("baseStatus", {}).get("state")  # "DONE" or "FAILED"

if state == "FAILED":
    activities = status.get("baseStatus", {}).get("activities", {})
    for name, info in activities.items():
        if info.get("firstFailure"):
            print(f"Error: {info['firstFailure'].get('message')}")

    # Or get full log
    print(job.get_log())
```

> **Important:** `recipe.run()` already waits for completion internally. Use `recipe.run(no_fail=True)` to prevent exceptions on failure, then inspect the returned job object.

## Detailed Error References

For full details on each error category including causes, code examples, and solutions:

- **[references/connection-errors.md](references/connection-errors.md)** — Connection refused, 401 Unauthorized, Project not found
- **[references/recipe-errors.md](references/recipe-errors.md)** — Settings not saved, empty output, job failures, job API usage patterns
- **[references/sql-errors.md](references/sql-errors.md)** — Invalid identifier (quoted/general), table does not exist, pre-join computed columns, insert value list mismatch
- **[references/environment-errors.md](references/environment-errors.md)** — ModuleNotFoundError, missing env vars, getting more help

## Scripts

- **[scripts/debug_job.py](../../scripts/debug_job.py)** — Standalone script to debug the most recent failed job
