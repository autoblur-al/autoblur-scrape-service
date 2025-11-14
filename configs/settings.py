from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    service_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Pydantic will also read from environment variables set in the system or by Kubernetes

settings = Settings()
