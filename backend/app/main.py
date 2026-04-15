import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import Base, engine
# Import all models so they are registered with Base
from app.models import User, Patient, Doctor, HealthData, Alert, Recommendation
from app.routes import all_routers

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare AI Monitoring Agent",
    description="Real-time patient monitoring and health insights with AI-powered recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
for router in all_routers:
    app.include_router(router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Healthcare AI Monitoring Agent API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/docs#/auth",
            "patients": "/docs#/patients",
            "health_data": "/docs#/health-data",
            "alerts": "/docs#/alerts",
            "recommendations": "/docs#/recommendations",
            "doctors": "/docs#/doctors"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False") == "True"
    )
