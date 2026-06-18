from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.database import engine, Base
from routers import upload, trendradar, status, results
from models.schemas import HealthResponse

# Lifespan context manager for startup and shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Automatically create database tables if they do not exist
    try:
        Base.metadata.create_all(bind=engine)
        print("Database connected successfully.")
    except Exception as e:
        print(f"WARNING: Could not connect to the database. Ensure DATABASE_URL is set correctly. Error: {e}")
    yield

app = FastAPI(
    title="ONYX Backend API",
    description="Backbone and TrendRadar Intelligence Module for ONYX platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
# For a hackathon project, we enable all origins, methods, and headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(upload.router)
app.include_router(trendradar.router)
app.include_router(status.router)
app.include_router(results.router)

# Health Check Route
@app.get("/api/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """
    Simple health check endpoint returning status and version.
    """
    return HealthResponse(status="ok", version="1.0.0")

# Root Route (For Railway Healthchecks)
@app.get("/", tags=["System"])
def root_check():
    """
    Root endpoint for default PaaS healthchecks (e.g. Railway).
    """
    return {"status": "ok", "service": "ONYX Backend"}
