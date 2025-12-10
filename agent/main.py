from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import agent, multimodal
from core.config import settings
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(agent.router, prefix="/api/v1/agent", tags=["agent"])
app.include_router(multimodal.router, prefix="/api/v1/multimodal", tags=["multimodal"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0.0"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
