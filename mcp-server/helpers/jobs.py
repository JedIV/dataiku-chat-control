"""Job and async operation handling utilities.

These helpers handle the tedious polling loops for builds, scenarios, and recipes.
"""

import time
from typing import Optional


def wait_for_job(job, timeout: int = 600, poll_interval: int = 2) -> dict:
    """Wait for a Dataiku job to complete.

    Args:
        job: A Dataiku job/future object with get_status() method
        timeout: Maximum seconds to wait (default 600)
        poll_interval: Seconds between status checks (default 2)

    Returns:
        dict with keys: success, status, duration, details
    """
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            return {
                "success": False,
                "status": "TIMEOUT",
                "duration": elapsed,
                "details": f"Job did not complete within {timeout} seconds"
            }

        status = job.get_status()
        state = status.get("baseStatus", {}).get("state", status.get("state", "UNKNOWN"))

        if state in ("DONE", "FAILED", "ABORTED"):
            return {
                "success": state == "DONE",
                "status": state,
                "duration": elapsed,
                "details": status
            }

        time.sleep(poll_interval)


def build_and_wait(client, project_key: str, dataset_name: str,
                   build_mode: str = "RECURSIVE_BUILD",
                   timeout: int = 600) -> dict:
    """Build a dataset and wait for completion.

    Args:
        client: DSSClient instance
        project_key: Project key
        dataset_name: Dataset to build
        build_mode: NON_RECURSIVE_FORCED_BUILD, RECURSIVE_BUILD, etc.
        timeout: Maximum seconds to wait

    Returns:
        dict with keys: success, status, duration, details
    """
    project = client.get_project(project_key)
    dataset = project.get_dataset(dataset_name)

    job = dataset.build(build_mode=build_mode)
    return wait_for_job(job, timeout=timeout)


def run_scenario_and_wait(client, project_key: str, scenario_id: str,
                          timeout: int = 600) -> dict:
    """Run a scenario and wait for completion.

    Args:
        client: DSSClient instance
        project_key: Project key
        scenario_id: Scenario ID to run
        timeout: Maximum seconds to wait

    Returns:
        dict with keys: success, status, duration, outcome, details
    """
    project = client.get_project(project_key)
    scenario = project.get_scenario(scenario_id)

    run = scenario.run()
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            return {
                "success": False,
                "status": "TIMEOUT",
                "duration": elapsed,
                "outcome": None,
                "details": f"Scenario did not complete within {timeout} seconds"
            }

        run_info = run.get_info()
        state = run_info.get("scenarioRun", {}).get("result", {}).get("outcome")

        if state is not None:
            return {
                "success": state == "SUCCESS",
                "status": "DONE",
                "duration": elapsed,
                "outcome": state,
                "details": run_info
            }

        time.sleep(2)


def run_recipe_and_wait(client, project_key: str, recipe_name: str,
                        timeout: int = 600) -> dict:
    """Run a recipe and wait for completion.

    Args:
        client: DSSClient instance
        project_key: Project key
        recipe_name: Recipe name to run
        timeout: Maximum seconds to wait

    Returns:
        dict with keys: success, status, duration, details
    """
    project = client.get_project(project_key)
    recipe = project.get_recipe(recipe_name)

    job = recipe.run()
    return wait_for_job(job, timeout=timeout)


def get_job_log(client, project_key: str, job_id: str) -> str:
    """Get the log output from a job.

    Args:
        client: DSSClient instance
        project_key: Project key
        job_id: Job ID

    Returns:
        Log content as string
    """
    project = client.get_project(project_key)
    job = project.get_job(job_id)
    return job.get_log()
