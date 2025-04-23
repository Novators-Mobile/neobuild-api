from fastapi import APIRouter

from app.api.endpoints import projects, releases, build

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(releases.router, prefix="/releases", tags=["releases"])
api_router.include_router(build.router, prefix="/build", tags=["build"]) 