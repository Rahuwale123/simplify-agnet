from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.config.settings import settings
from app.config.postgres_db import init_postgres_db


init_postgres_db()

app = FastAPI(
    title=settings.APP_NAME,
    description="A FastAPI wrapper for LangChain Agents",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    # Only watch the 'app' directory to avoid reloads when database files in 'data/' or 'main.py' change
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["app"], reload_excludes=["*.db", "*.db-journal", "data/*"])
