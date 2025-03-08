# app/main.py
from fastapi import FastAPI
from datetime import datetime, timezone


import uvicorn

# If you want to auto-create tables at startup (optional; 
# in production you'd typically use migrations with Alembic)
from app.core.db import engine
from app.models import Base

# Import routers from the routes folder
from app.routes import auth, category

# Create the database tables if they don't already exist
#Base.metadata.create_all(bind=engine)

app = FastAPI(title="Banco de Guayaquil Trusted Network Backend")

# Record the startup time for health-check purposes
startup_time = datetime.now(timezone.utc)

@app.get("/", tags=["Root"], summary="Health/Start Endpoint")
def read_root():
    """
    Simple health check endpoint to confirm the service is running.
    """
    return {
        "message": "Welcome to Banco de Guayaquil Trusted Network Backend API made by Team 'CoSierra Devs'! 🚀",
        "startup_time": startup_time.isoformat(),
    }

# Include the routers from separate files
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(category.router, prefix="/category", tags=["Category"])

def main():
    """
    Entry point for running with: `poetry run start` (or similar).
    """
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
