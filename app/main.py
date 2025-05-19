from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from app.core.config import settings
from app.routers import auth, projects, branches, tasks, releases
from app.database.session import engine, Base
from app.database.init_db import init_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize database with sample data (uncomment to use)
# init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(branches.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=settings.API_V1_STR)
app.include_router(releases.router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {"message": "Welcome to NeoBuild API", "docs": "/docs"}


if __name__ == "__main__":
    logger.info("Starting NeoBuild API")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 