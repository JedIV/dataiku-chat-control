"""
Import a SQL table as a dataset.

Usage:
    python import_sql_table.py <project_key> <connection> <schema> <table> [dataset_name]

Examples:
    python import_sql_table.py MYPROJECT sf-azure CRM CUSTOMERS
    python import_sql_table.py MYPROJECT sf-azure CRM CUSTOMERS my_customers
"""

import sys
from client import get_client


def list_schemas(connection_name: str, project_key: str = None):
    """List available schemas in a SQL connection."""
    client = get_client()
    # Need a project context to list schemas
    if project_key is None:
        projects = client.list_project_keys()
        if not projects:
            raise ValueError("No projects available")
        project_key = projects[0]

    project = client.get_project(project_key)
    schemas = project.list_sql_schemas(connection_name)
    return list(set(schemas))  # Remove duplicates


def list_tables(connection_name: str, schema_name: str, project_key: str = None):
    """List tables in a schema."""
    client = get_client()
    if project_key is None:
        projects = client.list_project_keys()
        if not projects:
            raise ValueError("No projects available")
        project_key = projects[0]

    project = client.get_project(project_key)
    tables = project.list_sql_tables(connection_name, schema_name=schema_name)
    return [t['table'] for t in tables]


def import_table(project_key: str, connection: str, schema: str, table: str, dataset_name: str = None):
    """Import a SQL table as a dataset with schema detection."""
    client = get_client()
    project = client.get_project(project_key)

    # Use tables import for proper schema detection
    import_def = project.init_tables_import()
    import_def.add_sql_table(connection=connection, schema=schema, table=table)

    # Prepare and mark as checked
    prepared = import_def.prepare()
    prepared.candidates['sqlImportCandidates'][0]['checked'] = True

    # Optionally rename the dataset
    if dataset_name:
        prepared.candidates['sqlImportCandidates'][0]['datasetName'] = dataset_name

    # Execute and wait
    result = prepared.execute()
    result.wait_for_result()

    final_name = dataset_name or table
    print(f"Imported table {schema}.{table} as dataset: {final_name}")

    return project.get_dataset(final_name)


def get_dataset_info(project_key: str, dataset_name: str):
    """Get schema and sample data from a dataset."""
    client = get_client()
    project = client.get_project(project_key)
    dataset = project.get_dataset(dataset_name)

    settings = dataset.get_settings()
    schema = settings.get_raw().get('schema', {}).get('columns', [])

    info = {
        'name': dataset_name,
        'columns': [(c['name'], c['type']) for c in schema],
        'sample': []
    }

    # Get sample rows
    col_names = [c['name'] for c in schema]
    try:
        for i, row in enumerate(dataset.iter_rows()):
            if i >= 5:
                break
            info['sample'].append({col_names[j]: row[j] for j in range(len(col_names))})
    except Exception:
        pass

    return info


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)

    project_key = sys.argv[1]
    connection = sys.argv[2]
    schema = sys.argv[3]
    table = sys.argv[4]
    dataset_name = sys.argv[5] if len(sys.argv) > 5 else None

    dataset = import_table(project_key, connection, schema, table, dataset_name)

    # Show info
    info = get_dataset_info(project_key, dataset_name or table)
    print(f"\nColumns ({len(info['columns'])}):")
    for name, dtype in info['columns']:
        print(f"  - {name} ({dtype})")

    if info['sample']:
        print(f"\nSample ({len(info['sample'])} rows):")
        for row in info['sample']:
            print(f"  {row}")

    print("\nDone!")
