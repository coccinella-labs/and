from __future__ import annotations

from datetime import datetime
import logging
from typing import Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from local_platform.builder import (
    build_ml_api_image,
    container_status,
    deploy_container,
    push_image_to_registry,
)

LOGGER = logging.getLogger("local_platform.control_plane")

APP_NAME = "ml-api"


class AppState(BaseModel):
    name: str
    status: str
    image_tag: str
    endpoint: str
    last_deploy: Optional[str]
    last_error: Optional[str]


app = FastAPI(title="Local Platform Control Plane", version="0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _default_state() -> AppState:
    return AppState(
        name=APP_NAME,
        status="idle",
        image_tag="ml-api-local:latest",
        endpoint="http://localhost:8080",
        last_deploy=None,
        last_error=None,
    )

APP_STATE = _default_state()


class DeployRequest(BaseModel):
    push_to_registry: bool = False
    registry: Optional[str] = None


def _background_deploy(push_to_registry: bool, registry: Optional[str]) -> None:
    global APP_STATE
    LOGGER.info("Starting deployment task push=%s registry=%s", push_to_registry, registry)
    APP_STATE.status = "building"
    try:
        image_tag = build_ml_api_image()
        APP_STATE.image_tag = image_tag
        deployed_tag = image_tag
        if push_to_registry:
            if not registry:
                raise HTTPException(status_code=400, detail="registry is required when pushing")
            deployed_tag = push_image_to_registry(registry)
            APP_STATE.image_tag = deployed_tag
        endpoint = deploy_container(deployed_tag)
        APP_STATE.endpoint = endpoint
        APP_STATE.last_deploy = datetime.utcnow().isoformat() + "Z"
        APP_STATE.status = "running"
        APP_STATE.last_error = None
        LOGGER.info("Deployment finished, app available at %s", endpoint)
    except Exception as exc:
        APP_STATE.status = "error"
        APP_STATE.last_error = str(exc)
        LOGGER.exception("Deployment failed")


@app.post("/deploy")
async def deploy(request: DeployRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(_background_deploy, request.push_to_registry, request.registry)
    return {"status": "scheduled", "request": request.dict()}


@app.get("/apps")
async def list_apps() -> AppState:
    return APP_STATE


@app.get("/status")
async def status():
    return {
        "control_plane": "healthy",
        "ml_api": container_status(),
        "app_state": APP_STATE.dict(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
