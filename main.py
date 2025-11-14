import uvicorn
from api.app import app
from configs.settings import Settings

if __name__ == "__main__":
    settings = Settings()
    uvicorn.run(
        app,
        host=settings.service_host if hasattr(settings, "service_host") else "0.0.0.0",
        port=settings.service_port if hasattr(settings, "service_port") else 8000,
        reload=True
    )
