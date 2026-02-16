from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Optional

ROOT_DIR = Path(__file__).resolve().parents[1]
ML_API_DIR = ROOT_DIR / "ml-api"
IMAGE_TAG = "ml-api-local:latest"
CONTAINER_NAME = "ml-api-local"
EXPOSE_PORT = 8080
ML_API_PORT = 8000

LOGGER = logging.getLogger("platform.builder")


def _run_command(command: list[str], cwd: Optional[Path] = None, check: bool = True) -> str:
    LOGGER.info("Running: %s", " ".join(command))
    process = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=check,
    )
    if process.stdout:
        LOGGER.debug(process.stdout.strip())
    if process.stderr:
        LOGGER.debug(process.stderr.strip())
    return process.stdout.strip()


def build_ml_api_image() -> str:
    """Build the ml-api Docker image using the existing Dockerfile."""
    if not ML_API_DIR.exists():
        raise FileNotFoundError(f"ml-api directory not found at {ML_API_DIR}")
    _run_command(["docker", "build", "-t", IMAGE_TAG, "."], cwd=ML_API_DIR)
    return IMAGE_TAG


def push_image_to_registry(registry: str) -> str:
    """Tag and push the image into a local registry."""
    remote_tag = f"{registry}/{IMAGE_TAG}"
    _run_command(["docker", "tag", IMAGE_TAG, remote_tag])
    _run_command(["docker", "push", remote_tag])
    return remote_tag


def stop_existing_container() -> None:
    """Stop + remove the previous container if it exists."""
    subprocess.run(
        ["docker", "rm", "-f", CONTAINER_NAME],
        check=False,
        capture_output=True,
        text=True,
    )


def deploy_container(image_tag: str = IMAGE_TAG) -> str:
    """Run the ml-api container locally on port 8080."""
    stop_existing_container()
    _run_command(
        [
            "docker",
            "run",
            "-d",
            "--name",
            CONTAINER_NAME,
            "-p",
            f"{EXPOSE_PORT}:{ML_API_PORT}",
            image_tag,
        ]
    )
    return f"http://localhost:{EXPOSE_PORT}"


def container_status() -> dict[str, str]:
    """Return basic container status information."""
    try:
        output = _run_command(["docker", "inspect", CONTAINER_NAME])
        return {"status": "running", "info": output}
    except subprocess.CalledProcessError:
        return {"status": "stopped", "info": "container not running"}
