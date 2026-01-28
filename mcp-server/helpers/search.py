"""Cross-project search and discovery utilities.

These helpers find things across the Dataiku instance.
"""

import re
from typing import Optional


def find_datasets(client, pattern: str, project_key: Optional[str] = None) -> list:
    """Find datasets matching a pattern.

    Args:
        client: DSSClient instance
        pattern: Regex pattern to match dataset names
        project_key: Optional project to limit search to

    Returns:
        list of dicts with project_key, name, type
    """
    regex = re.compile(pattern, re.IGNORECASE)
    results = []

    if project_key:
        projects = [{"projectKey": project_key}]
    else:
        projects = client.list_projects()

    for p in projects:
        pkey = p.get("projectKey")
        try:
            project = client.get_project(pkey)
            datasets = project.list_datasets()
            for d in datasets:
                name = d.get("name", "")
                if regex.search(name):
                    results.append({
                        "project_key": pkey,
                        "name": name,
                        "type": d.get("type")
                    })
        except:
            continue

    return results


def find_recipes(client, pattern: str, project_key: Optional[str] = None) -> list:
    """Find recipes matching a pattern.

    Args:
        client: DSSClient instance
        pattern: Regex pattern to match recipe names
        project_key: Optional project to limit search to

    Returns:
        list of dicts with project_key, name, type
    """
    regex = re.compile(pattern, re.IGNORECASE)
    results = []

    if project_key:
        projects = [{"projectKey": project_key}]
    else:
        projects = client.list_projects()

    for p in projects:
        pkey = p.get("projectKey")
        try:
            project = client.get_project(pkey)
            recipes = project.list_recipes()
            for r in recipes:
                name = r.get("name", "")
                if regex.search(name):
                    results.append({
                        "project_key": pkey,
                        "name": name,
                        "type": r.get("type")
                    })
        except:
            continue

    return results


def find_scenarios(client, pattern: str, project_key: Optional[str] = None) -> list:
    """Find scenarios matching a pattern.

    Args:
        client: DSSClient instance
        pattern: Regex pattern to match scenario names/IDs
        project_key: Optional project to limit search to

    Returns:
        list of dicts with project_key, id, name
    """
    regex = re.compile(pattern, re.IGNORECASE)
    results = []

    if project_key:
        projects = [{"projectKey": project_key}]
    else:
        projects = client.list_projects()

    for p in projects:
        pkey = p.get("projectKey")
        try:
            project = client.get_project(pkey)
            scenarios = project.list_scenarios()
            for s in scenarios:
                name = s.get("name", "")
                sid = s.get("id", "")
                if regex.search(name) or regex.search(sid):
                    results.append({
                        "project_key": pkey,
                        "id": sid,
                        "name": name
                    })
        except:
            continue

    return results


def find_by_connection(client, connection_name: str) -> list:
    """Find all datasets using a specific connection.

    Args:
        client: DSSClient instance
        connection_name: Name of the connection to search for

    Returns:
        list of dicts with project_key, name, type
    """
    results = []

    projects = client.list_projects()
    for p in projects:
        pkey = p.get("projectKey")
        try:
            project = client.get_project(pkey)
            datasets = project.list_datasets()
            for d in datasets:
                ds = project.get_dataset(d.get("name"))
                settings = ds.get_settings()
                params = settings.get_raw().get("params", {})
                if params.get("connection") == connection_name:
                    results.append({
                        "project_key": pkey,
                        "name": d.get("name"),
                        "type": d.get("type"),
                        "path": params.get("path") or params.get("table")
                    })
        except:
            continue

    return results


def find_by_type(client, dataset_type: str, project_key: Optional[str] = None) -> list:
    """Find all datasets of a specific type.

    Args:
        client: DSSClient instance
        dataset_type: Dataset type (e.g., "Snowflake", "PostgreSQL", "Filesystem")
        project_key: Optional project to limit search to

    Returns:
        list of dicts with project_key, name, connection
    """
    results = []

    if project_key:
        projects = [{"projectKey": project_key}]
    else:
        projects = client.list_projects()

    for p in projects:
        pkey = p.get("projectKey")
        try:
            project = client.get_project(pkey)
            datasets = project.list_datasets()
            for d in datasets:
                if d.get("type", "").lower() == dataset_type.lower():
                    ds = project.get_dataset(d.get("name"))
                    settings = ds.get_settings()
                    params = settings.get_raw().get("params", {})
                    results.append({
                        "project_key": pkey,
                        "name": d.get("name"),
                        "type": d.get("type"),
                        "connection": params.get("connection"),
                        "path": params.get("path") or params.get("table")
                    })
        except:
            continue

    return results


def find_users(client, pattern: str) -> list:
    """Find users matching a pattern.

    Args:
        client: DSSClient instance
        pattern: Regex pattern to match login or display name

    Returns:
        list of dicts with login, displayName, groups
    """
    regex = re.compile(pattern, re.IGNORECASE)
    results = []

    users = client.list_users()
    for u in users:
        login = u.get("login", "")
        display = u.get("displayName", "")
        if regex.search(login) or regex.search(display):
            results.append({
                "login": login,
                "displayName": display,
                "groups": u.get("groups", []),
                "email": u.get("email")
            })

    return results
