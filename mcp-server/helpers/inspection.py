"""Data exploration and inspection utilities.

These helpers combine multiple API calls into single useful views.
"""

from typing import Optional


def dataset_info(client, project_key: str, dataset_name: str,
                 sample_size: int = 5) -> dict:
    """Get comprehensive information about a dataset.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset name
        sample_size: Number of sample rows to include

    Returns:
        dict with keys: name, type, schema, row_count, sample, connection, path
    """
    project = client.get_project(project_key)
    dataset = project.get_dataset(dataset_name)
    settings = dataset.get_settings()

    # Get schema
    schema = settings.get_raw().get("schema", {}).get("columns", [])
    columns = [(col.get("name"), col.get("type")) for col in schema]

    # Get dataset type and connection info
    ds_type = settings.type
    params = settings.get_raw().get("params", {})
    connection = params.get("connection")
    path = params.get("path") or params.get("table")

    # Try to get row count and sample
    row_count = None
    sample = []
    try:
        # Get metrics for row count
        metrics = dataset.get_last_metric_values()
        if metrics:
            records_metric = metrics.get_global_value("records:COUNT_RECORDS")
            if records_metric:
                row_count = records_metric
    except:
        pass

    try:
        # Get sample rows (iter_rows doesn't support limit param)
        sample = []
        for i, row in enumerate(dataset.iter_rows()):
            if i >= sample_size:
                break
            # Convert list to dict if needed
            if isinstance(row, dict):
                sample.append(row)
            else:
                sample.append(dict(zip([c[0] for c in columns], row)))
    except:
        pass

    return {
        "name": dataset_name,
        "type": ds_type,
        "schema": columns,
        "row_count": row_count,
        "sample": sample,
        "connection": connection,
        "path": path
    }


def project_summary(client, project_key: str) -> dict:
    """Get a summary of a project's contents and status.

    Args:
        client: DSSClient instance
        project_key: Project key

    Returns:
        dict with keys: name, datasets, recipes, scenarios, jobs, status
    """
    project = client.get_project(project_key)

    # Get project metadata
    metadata = project.get_metadata()

    # List all objects
    datasets = project.list_datasets()
    recipes = project.list_recipes()
    scenarios = project.list_scenarios()

    # Get recent jobs
    jobs = []
    try:
        job_list = project.list_jobs()
        jobs = job_list[:5] if job_list else []
    except:
        pass

    return {
        "key": project_key,
        "name": metadata.get("label", project_key),
        "description": metadata.get("description", ""),
        "datasets": [{"name": d.get("name"), "type": d.get("type")} for d in datasets],
        "recipes": [{"name": r.get("name"), "type": r.get("type")} for r in recipes],
        "scenarios": [{"id": s.get("id"), "name": s.get("name")} for s in scenarios],
        "recent_jobs": jobs,
        "dataset_count": len(datasets),
        "recipe_count": len(recipes),
        "scenario_count": len(scenarios)
    }


def list_projects_summary(client) -> list:
    """Get a summary of all projects.

    Args:
        client: DSSClient instance

    Returns:
        list of dicts with project info
    """
    projects = client.list_projects()

    summaries = []
    for p in projects:
        summaries.append({
            "key": p.get("projectKey"),
            "name": p.get("name"),
            "owner": p.get("ownerLogin"),
            "last_modified": p.get("versionTag", {}).get("lastModifiedOn")
        })

    return summaries


def connection_info(client, connection_name: str) -> dict:
    """Get information about a connection.

    Args:
        client: DSSClient instance
        connection_name: Name of the connection

    Returns:
        dict with keys: name, type, usable, details
    """
    conn = client.get_connection(connection_name)
    definition = conn.get_definition()

    # Test connection
    test_result = None
    try:
        test_result = conn.test()
    except Exception as e:
        test_result = {"ok": False, "error": str(e)}

    return {
        "name": connection_name,
        "type": definition.get("type"),
        "usable_by": definition.get("usableBy"),
        "params": {k: v for k, v in definition.get("params", {}).items()
                   if k not in ("password", "secretKey", "privateKey")},
        "test_result": test_result
    }


def list_connections_summary(client) -> list:
    """Get a summary of all connections.

    Args:
        client: DSSClient instance

    Returns:
        list of dicts with connection info
    """
    connections = client.list_connections()

    # list_connections returns a dict {name: definition}
    return [
        {
            "name": name,
            "type": defn.get("type"),
            "usable_by": defn.get("usableBy")
        }
        for name, defn in connections.items()
    ]


def user_info(client, login: Optional[str] = None) -> dict:
    """Get information about a user (or current user if not specified).

    Args:
        client: DSSClient instance
        login: User login (optional, defaults to current user)

    Returns:
        dict with user information
    """
    if login:
        user = client.get_user(login)
        return user.get_settings().get_raw()
    else:
        return client.get_own_user().get_settings().get_raw()
