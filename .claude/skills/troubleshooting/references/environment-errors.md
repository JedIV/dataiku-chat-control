# Environment Errors

## "ModuleNotFoundError: dataikuapi"
```
ModuleNotFoundError: No module named 'dataikuapi'
```

**Cause:** Virtual environment not activated

**Solution:**
```bash
source ~/dataiku-env/bin/activate && export $(grep -v '^#' .env | xargs)
```

## "KeyError: 'DSS_URL'"
```
KeyError: 'DSS_URL'
```

**Cause:** Environment variable not set

**Solution:**
```bash
# Check variables
echo $DSS_URL
echo $DSS_API_KEY
echo $DSS_PROJECT_KEY

# Load from .env
export $(grep -v '^#' .env | xargs)
```

## Getting More Help

1. **Job logs**: `job.get_log()` or check Dataiku UI
2. **API methods**: Inspect the installed `dataikuapi` package
3. **Recipe settings**: `print(settings.get_recipe_params())`
4. **Dataset info**: `print(dataset.get_settings().get_raw())`
