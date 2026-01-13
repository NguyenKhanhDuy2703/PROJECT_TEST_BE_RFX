from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    PROJECT_NAME: str = " PROJECT MANAGEMENT SYSTEM "
    POSTGRES_USER : str = "postgres"
    POSTGRES_PASSWORD : str = "123456"
    POSTGRES_SERVER : str = "localhost"
    POSTGRES_PORT : str = "5432"
    POSTGRES_DB : str = "rfx_db"
    print("Configuration settings loaded successfully.")
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()