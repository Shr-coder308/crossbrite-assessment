from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/crossbrite"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "crossbrite-development-secret-key-change-in-production"

    class Config:
        env_file = ".env"


settings = Settings()