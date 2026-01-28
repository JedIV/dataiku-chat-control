"""
Dataiku API client wrapper.

Provides a configured DSSClient instance using credentials from environment variables.
"""

import os
from dotenv import load_dotenv
import dataikuapi

# Load environment variables from .env file
load_dotenv()


def get_client() -> dataikuapi.DSSClient:
    """
    Create and return a configured DSSClient instance.

    Uses DATAIKU_URL and DATAIKU_API_KEY from environment variables.
    """
    url = os.environ.get("DATAIKU_URL")
    api_key = os.environ.get("DATAIKU_API_KEY")

    if not url or not api_key:
        raise ValueError(
            "DATAIKU_URL and DATAIKU_API_KEY must be set in environment or .env file"
        )

    return dataikuapi.DSSClient(url, api_key)


if __name__ == "__main__":
    # Quick connection test
    client = get_client()
    print(f"Connected to: {os.environ.get('DATAIKU_URL')}")
    print(f"Projects: {client.list_project_keys()}")
