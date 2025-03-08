from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BG CoSierra - Corporate Trusted Network",
    description="Backend API for Banco de Guayaquil's B2B trusted network platform"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the CoSierra Trusted Network API"}

# Import and include routers
from app.api import auth, users, network, providers

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(network.router)
app.include_router(providers.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)