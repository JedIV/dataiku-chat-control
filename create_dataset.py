"""
Create a new managed dataset with CSV data.

Usage:
    python create_dataset.py <project_key> <dataset_name> <csv_file_or_data>

Examples:
    python create_dataset.py MYPROJECT customers data.csv
    python create_dataset.py MYPROJECT sales '{"columns": ["id", "amount"], "rows": [[1, 100], [2, 200]]}'
"""

import sys
import io
import csv
import json
from client import get_client


def create_dataset_from_csv(project_key: str, dataset_name: str, csv_content: str, connection: str = "filesystem_managed"):
    """Create a managed dataset from CSV content."""
    client = get_client()
    project = client.get_project(project_key)

    # Delete if exists
    existing = [d["name"] for d in project.list_datasets()]
    if dataset_name in existing:
        print(f"Deleting existing dataset: {dataset_name}")
        project.get_dataset(dataset_name).delete()

    # Create upload dataset
    dataset = project.create_upload_dataset(dataset_name, connection)

    # Upload CSV
    csv_bytes = io.BytesIO(csv_content.encode('utf-8'))
    dataset.uploaded_add_file(csv_bytes, f"{dataset_name}.csv")

    print(f"Created dataset: {dataset_name}")
    return dataset


def create_dataset_from_dict(project_key: str, dataset_name: str, columns: list, rows: list, connection: str = "filesystem_managed"):
    """Create a managed dataset from column names and row data."""
    # Convert to CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)
    csv_content = output.getvalue()

    return create_dataset_from_csv(project_key, dataset_name, csv_content, connection)


def create_dataset_from_records(project_key: str, dataset_name: str, records: list[dict], connection: str = "filesystem_managed"):
    """Create a managed dataset from a list of dictionaries."""
    if not records:
        raise ValueError("Records list cannot be empty")

    columns = list(records[0].keys())
    rows = [[r.get(c) for c in columns] for r in records]

    return create_dataset_from_dict(project_key, dataset_name, columns, rows, connection)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    project_key = sys.argv[1]
    dataset_name = sys.argv[2]
    data_source = sys.argv[3]

    # Check if it's a file or JSON data
    if data_source.endswith('.csv'):
        with open(data_source, 'r') as f:
            csv_content = f.read()
        create_dataset_from_csv(project_key, dataset_name, csv_content)
    elif data_source.startswith('{'):
        data = json.loads(data_source)
        if 'records' in data:
            create_dataset_from_records(project_key, dataset_name, data['records'])
        else:
            create_dataset_from_dict(project_key, dataset_name, data['columns'], data['rows'])
    else:
        # Assume it's a file path
        with open(data_source, 'r') as f:
            csv_content = f.read()
        create_dataset_from_csv(project_key, dataset_name, csv_content)

    print("Done!")
