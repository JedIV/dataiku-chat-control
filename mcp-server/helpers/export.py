"""Data extraction and export utilities.

These helpers get data out of Dataiku in useful formats.
"""

from typing import Optional


def to_records(client, project_key: str, dataset_name: str,
               limit: int = 100) -> list:
    """Get dataset rows as a list of dictionaries.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset name
        limit: Maximum rows to return (default 100)

    Returns:
        list of dicts, one per row
    """
    project = client.get_project(project_key)
    dataset = project.get_dataset(dataset_name)

    # Get schema to build dicts (iter_rows returns lists, not dicts)
    settings = dataset.get_settings()
    schema = settings.get_raw().get("schema", {}).get("columns", [])
    col_names = [col.get("name") for col in schema]

    rows = []
    for i, row in enumerate(dataset.iter_rows()):
        if i >= limit:
            break
        # Convert list to dict
        if isinstance(row, dict):
            rows.append(row)
        else:
            rows.append(dict(zip(col_names, row)))
    return rows


def sample(client, project_key: str, dataset_name: str, n: int = 10) -> list:
    """Get a sample of rows from a dataset.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset name
        n: Number of rows to sample

    Returns:
        list of dicts, one per row
    """
    return to_records(client, project_key, dataset_name, limit=n)


def get_schema(client, project_key: str, dataset_name: str) -> list:
    """Get the schema of a dataset.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset name

    Returns:
        list of (column_name, column_type) tuples
    """
    project = client.get_project(project_key)
    dataset = project.get_dataset(dataset_name)
    settings = dataset.get_settings()

    schema = settings.get_raw().get("schema", {}).get("columns", [])
    return [(col.get("name"), col.get("type")) for col in schema]


def get_column_names(client, project_key: str, dataset_name: str) -> list:
    """Get just the column names of a dataset.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset name

    Returns:
        list of column names
    """
    schema = get_schema(client, project_key, dataset_name)
    return [name for name, _ in schema]


def count_rows(client, project_key: str, dataset_name: str) -> Optional[int]:
    """Get the row count of a dataset.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset name

    Returns:
        int row count or None if not available
    """
    project = client.get_project(project_key)
    dataset = project.get_dataset(dataset_name)

    try:
        metrics = dataset.get_last_metric_values()
        if metrics:
            return metrics.get_global_value("records:COUNT_RECORDS")
    except:
        pass

    return None


def head(client, project_key: str, dataset_name: str, n: int = 5) -> None:
    """Print the first n rows of a dataset in a readable format.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset name
        n: Number of rows to show
    """
    schema = get_schema(client, project_key, dataset_name)
    rows = to_records(client, project_key, dataset_name, limit=n)

    if not rows:
        print("(empty dataset)")
        return

    # Print header
    columns = [name for name, _ in schema]
    print(" | ".join(columns))
    print("-" * (sum(len(c) for c in columns) + 3 * (len(columns) - 1)))

    # Print rows
    for row in rows:
        values = [str(row.get(col, ""))[:30] for col in columns]
        print(" | ".join(values))


def describe(client, project_key: str, dataset_name: str) -> dict:
    """Get a statistical description of a dataset.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset name

    Returns:
        dict with schema, row_count, and sample
    """
    schema = get_schema(client, project_key, dataset_name)
    row_count = count_rows(client, project_key, dataset_name)
    sample_rows = sample(client, project_key, dataset_name, n=5)

    return {
        "columns": len(schema),
        "schema": schema,
        "row_count": row_count,
        "sample": sample_rows
    }


def to_csv_string(client, project_key: str, dataset_name: str,
                  limit: int = 100) -> str:
    """Export dataset rows as a CSV string.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset name
        limit: Maximum rows to export

    Returns:
        CSV formatted string
    """
    import csv
    from io import StringIO

    schema = get_schema(client, project_key, dataset_name)
    columns = [name for name, _ in schema]
    rows = to_records(client, project_key, dataset_name, limit=limit)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue()
