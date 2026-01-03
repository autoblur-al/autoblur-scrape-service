from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    service_port: int = 8000
    service_host: str = "0.0.0.0"
    car_image_save_dir: str = "static/images"  # default, can be overridden by env

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Pydantic will also read from environment variables set in the system or by Kubernetes
        fields = {"car_image_save_dir": {"env": "CAR_IMAGE_SAVE_DIR"}}


settings = Settings()
